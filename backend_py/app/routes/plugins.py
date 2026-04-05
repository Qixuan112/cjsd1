"""
插件路由模块（公开端）

提供插件相关的公开 API 端点，不需要认证
"""

from flask import Blueprint, request, jsonify

from app.services.plugin_service import (
    get_plugins,
    get_plugin_by_id,
    fetch_github_readme,
    fetch_github_stats
)

bp = Blueprint('plugins', __name__)


@bp.route('', methods=['GET'])
def list_plugins():
    """
    获取插件列表接口
    
    支持分页、搜索、分类筛选、排序
    只返回 status='approved' 的插件
    
    Query Parameters:
        - page: 页码（默认1）
        - limit: 每页数量（默认20）
        - search: 搜索关键词
        - category: 分类ID或名称
        - sortBy: 排序方式（stars/updated/name）
    
    Response:
        {
            "items": [
                {
                    "id": 1,
                    "name": "Plugin Name",
                    "description": "...",
                    "category": "Tools",
                    "author": "username",
                    "status": "approved",
                    "version": "1.0.0",
                    "stars": 100,
                    "forks": 20,
                    "created_at": "2024-01-01T00:00:00Z"
                }
            ],
            "total": 100,
            "page": 1,
            "limit": 20
        }
    """
    # 获取查询参数
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
    except ValueError:
        return jsonify({'error': 'Invalid page or limit parameter'}), 400
    
    # 限制每页最大数量
    if limit > 100:
        limit = 100
    
    search = request.args.get('search', None)
    category = request.args.get('category', None)
    sort_by = request.args.get('sortBy', None)
    
    # 验证排序参数
    valid_sort_options = ['stars', 'updated', 'name', None]
    if sort_by not in valid_sort_options:
        return jsonify({'error': 'Invalid sortBy parameter. Allowed: stars, updated, name'}), 400
    
    # 获取插件列表
    result = get_plugins(
        page=page,
        limit=limit,
        search=search,
        category=category,
        sort_by=sort_by
    )
    
    return jsonify(result), 200


@bp.route('/<int:plugin_id>', methods=['GET'])
def get_plugin_detail(plugin_id: int):
    """
    获取插件详情接口
    
    返回插件详情，包括 GitHub 数据和 README 内容
    只返回 status='approved' 的插件
    
    Path Parameters:
        - id: 插件ID
    
    Response:
        {
            "id": 1,
            "name": "Plugin Name",
            "description": "...",
            "repo_url": "https://github.com/...",
            "category_id": 1,
            "category": "Tools",
            "author_id": 1,
            "author": "username",
            "status": "approved",
            "manifest": {...},
            "github_data": {
                "stars": 100,
                "forks": 20,
                "last_updated": "2024-01-01T00:00:00Z",
                "open_issues": 5,
                "language": "Python",
                "description": "...",
                "homepage": "...",
                "license": "MIT"
            },
            "version": "1.0.0",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "readme": "# README Content..."
        }
    """
    # 获取插件
    plugin = get_plugin_by_id(plugin_id)
    
    if not plugin:
        return jsonify({'error': 'Plugin not found'}), 404
    
    # 构建响应数据
    result = plugin.to_dict()
    
    # 获取 README 内容
    readme = None
    if plugin.repo_url:
        readme = fetch_github_readme(plugin.repo_url)
    
    result['readme'] = readme
    
    return jsonify(result), 200
