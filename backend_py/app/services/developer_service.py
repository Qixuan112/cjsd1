"""
开发者服务模块

提供开发者相关的业务逻辑，包括插件提交、列表获取和撤回功能
"""

import re
import requests
from typing import Optional
from sqlalchemy import desc

from app import db
from app.models.plugin import Plugin, PluginStatus
from app.models.audit_log import AuditLog, AuditAction, ResourceType
from app.services.plugin_service import fetch_github_stats


def _parse_github_repo_url(repo_url: str) -> Optional[tuple[str, str]]:
    """
    解析 GitHub 仓库 URL，提取 owner 和 repo
    
    Args:
        repo_url: GitHub 仓库 URL
    
    Returns:
        (owner, repo) 元组或 None
    """
    patterns = [
        r'github\.com/([^/]+)/([^/]+)/?',
        r'github\.com/([^/]+)/([^/]+)\.git',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, repo_url)
        if match:
            owner = match.group(1)
            repo = match.group(2).replace('.git', '')
            return (owner, repo)
    
    return None


def validate_github_repo(repo_url: str) -> tuple[bool, Optional[dict]]:
    """
    验证 GitHub 仓库是否存在且可访问
    
    Args:
        repo_url: GitHub 仓库 URL
    
    Returns:
        (是否有效, 仓库信息或错误信息)
    """
    repo_info = _parse_github_repo_url(repo_url)
    if not repo_info:
        return False, {'error': 'Invalid GitHub repository URL format'}
    
    owner, repo = repo_info
    api_url = f'https://api.github.com/repos/{owner}/{repo}'
    
    try:
        response = requests.get(
            api_url,
            timeout=10,
            headers={'Accept': 'application/vnd.github.v3+json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            return True, {
                'owner': owner,
                'repo': repo,
                'stars': data.get('stargazers_count', 0),
                'forks': data.get('forks_count', 0),
                'description': data.get('description'),
                'last_updated': data.get('updated_at'),
                'open_issues': data.get('open_issues_count', 0),
                'language': data.get('language'),
                'homepage': data.get('homepage'),
                'license': data.get('license', {}).get('name') if data.get('license') else None
            }
        elif response.status_code == 404:
            return False, {'error': 'Repository not found'}
        elif response.status_code == 403:
            return False, {'error': 'GitHub API rate limit exceeded or access denied'}
        else:
            return False, {'error': f'GitHub API error: {response.status_code}'}
    except requests.RequestException as e:
        return False, {'error': f'Failed to connect to GitHub: {str(e)}'}
    except Exception as e:
        return False, {'error': f'Unexpected error: {str(e)}'}


def submit_plugin(user_id: int, data: dict) -> tuple[bool, dict]:
    """
    提交新插件
    
    验证 GitHub 仓库存在且可访问，获取仓库信息，创建插件记录
    
    Args:
        user_id: 用户ID
        data: 插件数据 {name, description, repo_url, category_id}
    
    Returns:
        (是否成功, 插件信息或错误信息)
    """
    name = data.get('name')
    description = data.get('description')
    repo_url = data.get('repo_url')
    category_id = data.get('category_id')
    
    # 验证必填字段
    if not name or not name.strip():
        return False, {'error': 'Plugin name is required'}
    
    if not repo_url or not repo_url.strip():
        return False, {'error': 'Repository URL is required'}
    
    # 验证 GitHub 仓库
    is_valid, repo_info = validate_github_repo(repo_url)
    if not is_valid:
        return False, repo_info
    
    # 检查插件名称是否已存在
    existing_plugin = db.session.query(Plugin).filter(
        Plugin.name == name.strip()
    ).first()
    if existing_plugin:
        return False, {'error': 'Plugin name already exists'}
    
    # 创建插件记录
    plugin = Plugin(
        name=name.strip(),
        description=description.strip() if description else None,
        repo_url=repo_url.strip(),
        category_id=category_id,
        author_id=user_id,
        status=PluginStatus.pending,
        github_data={
            'stars': repo_info.get('stars', 0),
            'forks': repo_info.get('forks', 0),
            'last_updated': repo_info.get('last_updated'),
            'open_issues': repo_info.get('open_issues', 0),
            'language': repo_info.get('language'),
            'license': repo_info.get('license'),
        }
    )
    
    db.session.add(plugin)
    db.session.flush()  # 获取 plugin.id
    
    # 记录审计日志
    AuditLog.log(
        user_id=user_id,
        action=AuditAction.submit,
        resource_type=ResourceType.plugin.value,
        resource_id=plugin.id,
        details={
            'plugin_name': plugin.name,
            'repo_url': plugin.repo_url,
            'github_data': plugin.github_data
        }
    )
    
    db.session.commit()
    
    return True, plugin.to_dict()


def get_my_plugins(user_id: int, page: int = 1, limit: int = 20) -> dict:
    """
    获取我的插件列表
    
    Args:
        user_id: 用户ID
        page: 页码（默认1）
        limit: 每页数量（默认20）
    
    Returns:
        {
            'items': [],
            'total': 0,
            'page': 1,
            'limit': 20
        }
    """
    # 构建查询
    query = db.session.query(Plugin).filter(Plugin.author_id == user_id)
    
    # 计算总数
    total = query.count()
    
    # 按创建时间降序排序
    query = query.order_by(desc(Plugin.created_at))
    
    # 分页
    offset = (page - 1) * limit
    plugins = query.offset(offset).limit(limit).all()
    
    return {
        'items': [plugin.to_dict() for plugin in plugins],
        'total': total,
        'page': page,
        'limit': limit
    }


def withdraw_plugin(user_id: int, plugin_id: int) -> tuple[bool, dict]:
    """
    撤回插件
    
    只能撤回自己创建的且状态为 pending 的插件
    
    Args:
        user_id: 用户ID
        plugin_id: 插件ID
    
    Returns:
        (是否成功, 结果信息或错误信息)
    """
    plugin = db.session.query(Plugin).get(plugin_id)
    
    if not plugin:
        return False, {'error': 'Plugin not found'}
    
    # 检查是否是插件创建者
    if plugin.author_id != user_id:
        return False, {'error': 'Permission denied: you can only withdraw your own plugins'}
    
    # 检查插件状态是否为 pending
    if plugin.status != PluginStatus.pending:
        return False, {'error': f'Cannot withdraw plugin with status: {plugin.status.value}. Only pending plugins can be withdrawn.'}
    
    # 删除插件
    db.session.delete(plugin)
    
    # 记录审计日志
    AuditLog.log(
        user_id=user_id,
        action=AuditAction.reject,  # 使用 reject 动作表示撤回
        resource_type=ResourceType.plugin.value,
        resource_id=plugin_id,
        details={
            'action_type': 'withdraw',
            'plugin_name': plugin.name,
            'previous_status': plugin.status.value
        }
    )
    
    db.session.commit()
    
    return True, {'message': 'Plugin withdrawn successfully'}
