/**
 * 插件市场 - 前端应用核心
 */

// API 配置
const API_BASE_URL = '/api';

// 存储键名
const STORAGE_KEYS = {
  TOKEN: 'plugin_marketplace_token',
  REFRESH_TOKEN: 'plugin_marketplace_refresh_token',
  USER: 'plugin_marketplace_user',
  TOKEN_EXPIRES: 'plugin_marketplace_token_expires'
};

/**
 * API 请求工具
 */
const api = {
  // 标记是否正在刷新 Token
  _isRefreshing: false,
  // 等待 Token 刷新的请求队列
  _refreshQueue: [],

  async request(url, options = {}) {
    // 检查 Token 是否需要刷新
    await this._checkAndRefreshToken();

    const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(`${API_BASE_URL}${url}`, {
        ...options,
        headers
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Token 过期，尝试刷新
          const refreshed = await this._handleTokenExpired();
          if (refreshed) {
            // 刷新成功，重试请求
            return this.request(url, options);
          } else {
            // 刷新失败，清除登录状态并跳转
            auth.logout();
            window.location.href = '/login.html';
            return;
          }
        }
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      // 处理 204 No Content 响应
      if (response.status === 204) {
        return null;
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  // 检查 Token 是否需要刷新
  async _checkAndRefreshToken() {
    const expiresAt = localStorage.getItem(STORAGE_KEYS.TOKEN_EXPIRES);
    if (!expiresAt) return;

    const expiresTime = parseInt(expiresAt);
    const now = Date.now();
    const fiveMinutes = 5 * 60 * 1000;

    // 如果 Token 将在 5 分钟内过期，提前刷新
    if (expiresTime - now < fiveMinutes) {
      await this._refreshToken();
    }
  },

  // 处理 Token 过期
  async _handleTokenExpired() {
    if (this._isRefreshing) {
      // 如果正在刷新，等待刷新完成
      return new Promise((resolve) => {
        this._refreshQueue.push(resolve);
      });
    }
    return this._refreshToken();
  },

  // 刷新 Token
  async _refreshToken() {
    const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
    if (!refreshToken) {
      return false;
    }

    this._isRefreshing = true;

    try {
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh_token: refreshToken })
      });

      if (!response.ok) {
        throw new Error('Refresh failed');
      }

      const data = await response.json();

      // 更新 Token
      localStorage.setItem(STORAGE_KEYS.TOKEN, data.access_token);
      // 更新过期时间（假设 Token 有效期为 1 小时）
      const expiresAt = Date.now() + 60 * 60 * 1000;
      localStorage.setItem(STORAGE_KEYS.TOKEN_EXPIRES, expiresAt.toString());

      // 通知等待的请求
      this._refreshQueue.forEach(resolve => resolve(true));
      this._refreshQueue = [];

      return true;
    } catch (error) {
      console.error('Token refresh failed:', error);
      // 通知等待的请求刷新失败
      this._refreshQueue.forEach(resolve => resolve(false));
      this._refreshQueue = [];
      return false;
    } finally {
      this._isRefreshing = false;
    }
  },

  get(url) {
    return this.request(url, { method: 'GET' });
  },

  post(url, data) {
    return this.request(url, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },

  put(url, data) {
    return this.request(url, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  },

  delete(url) {
    return this.request(url, { method: 'DELETE' });
  }
};

/**
 * 认证管理
 */
const auth = {
  getToken() {
    return localStorage.getItem(STORAGE_KEYS.TOKEN);
  },
  
  getUser() {
    const userJson = localStorage.getItem(STORAGE_KEYS.USER);
    return userJson ? JSON.parse(userJson) : null;
  },
  
  setAuth(token, user, refreshToken = null) {
    localStorage.setItem(STORAGE_KEYS.TOKEN, token);
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
    if (refreshToken) {
      localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refreshToken);
    }
    // 设置 Token 过期时间（假设有效期为 1 小时）
    const expiresAt = Date.now() + 60 * 60 * 1000;
    localStorage.setItem(STORAGE_KEYS.TOKEN_EXPIRES, expiresAt.toString());
  },

  logout() {
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER);
    localStorage.removeItem(STORAGE_KEYS.TOKEN_EXPIRES);
  },
  
  isAuthenticated() {
    return !!this.getToken();
  },
  
  hasRole(role) {
    const user = this.getUser();
    if (!user) return false;
    
    const roleHierarchy = {
      'user': 1,
      'developer': 2,
      'reviewer': 3,
      'admin': 4
    };
    
    return roleHierarchy[user.role] >= roleHierarchy[role];
  }
};

/**
 * 工具函数
 */
const utils = {
  /**
   * 格式化日期
   */
  formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    const now = new Date();
    const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return '今天';
    if (diffDays === 1) return '昨天';
    if (diffDays < 7) return `${diffDays} 天前`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} 周前`;
    return `${Math.floor(diffDays / 30)} 月前`;
  },
  
  /**
   * 格式化时间（精确到分钟）
   */
  formatTimeAgo(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return '刚刚';
    if (diffMins < 60) return `${diffMins} 分钟前`;
    if (diffHours < 24) return `${diffHours} 小时前`;
    if (diffDays < 30) return `${diffDays} 天前`;
    return date.toLocaleDateString('zh-CN');
  },
  
  /**
   * 获取状态标签样式
   */
  getStatusBadge(status) {
    const statusMap = {
      'pending': { text: '待审核', class: 'badge-warning' },
      'approved': { text: '已通过', class: 'badge-success' },
      'rejected': { text: '已驳回', class: 'badge-error' },
      'removed': { text: '已下架', class: 'badge-default' },
      'draft': { text: '草稿', class: 'badge-default' }
    };
    return statusMap[status] || { text: status, class: 'badge-default' };
  },
  
  /**
   * 获取分类名称
   */
  getCategoryName(slug) {
    const names = {
      'productivity': '生产力',
      'developer-tools': '开发工具',
      'design': '设计',
      'communication': '通讯',
      'utilities': '实用工具'
    };
    return names[slug] || slug;
  },
  
  /**
   * 防抖函数
   */
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },
  
  /**
   * 显示加载状态
   */
  showLoading(container, text = '加载中...') {
    container.innerHTML = `
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <p class="loading-text">${text}</p>
      </div>
    `;
  },
  
  /**
   * 显示错误状态
   */
  showError(container, message, onRetry) {
    container.classList.remove('plugin-grid');
    container.classList.add('error-container');
    container.innerHTML = `
      <div class="empty-state">
        <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
        <h3 class="empty-title">出错了</h3>
        <p class="empty-description">${message}</p>
        ${onRetry ? `<button class="btn btn-primary" onclick="${onRetry}">重试</button>` : ''}
      </div>
    `;
  },
  
  /**
   * 显示空状态
   */
  showEmpty(container, message) {
    container.innerHTML = `
      <div class="empty-state">
        <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
        </svg>
        <h3 class="empty-title">暂无数据</h3>
        <p class="empty-description">${message}</p>
      </div>
    `;
  }
};

/**
 * 页面初始化
 */
document.addEventListener('DOMContentLoaded', () => {
  // 更新用户界面
  updateUserUI();
});

/**
 * 更新用户界面（显示登录状态）
 */
function updateUserUI() {
  const user = auth.getUser();
  const userContainers = document.querySelectorAll('.user-container');
  
  userContainers.forEach(container => {
    if (user) {
      // 根据角色构建导航按钮
      let navButtons = '<a href="developer.html" class="btn btn-ghost btn-sm">开发者中心</a>';
      
      // 审批者/管理员显示审批插件按钮
      if (user.role === 'reviewer' || user.role === 'admin') {
        navButtons += '<a href="review-plugins.html" class="btn btn-ghost btn-sm">审批插件</a>';
      }
      
      // 管理员显示管理层按钮
      if (user.role === 'admin') {
        navButtons += '<a href="admin.html" class="btn btn-ghost btn-sm">管理层</a>';
      }
      
      container.innerHTML = `
        <div class="flex items-center gap-2">
          ${navButtons}
          <img src="${user.avatar || 'https://avatars.githubusercontent.com/u/0?v=4'}" alt="${user.username}" class="w-5 h-5 rounded-full">
          <span class="text-sm">${user.username}</span>
          <button class="btn btn-ghost btn-sm" onclick="auth.logout(); window.location.href='/'">退出</button>
        </div>
      `;
    } else {
      container.innerHTML = `
        <a href="/login.html" class="btn btn-primary btn-sm">登录</a>
      `;
    }
  });
}

// 导出全局变量
window.api = api;
window.auth = auth;
window.utils = utils;
