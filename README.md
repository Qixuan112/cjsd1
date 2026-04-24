# 🔌 插件市场 (Plugin Marketplace)

<p align="center">
  <b>一个功能完善的插件市场系统，支持插件的提交、审核、发布和管理。</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Flask-2.0+-green.svg" alt="Flask 2.0+">
  <img src="https://img.shields.io/badge/MySQL-5.7+-orange.svg" alt="MySQL 5.7+">
  <img src="https://img.shields.io/badge/License-AGPL--3.0-yellow.svg" alt="License: AGPL-3.0">
</p>

<p align="center">
  <a href="#-功能特性">功能特性</a> •
  <a href="#-项目架构">项目架构</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-文档">文档</a> •
  <a href="#-api-概览">API</a>
</p>

---

## ✨ 功能特性

- **🔐 用户认证** - 基于 GitHub OAuth 的登录系统，JWT 身份验证，支持 Access Token 和 Refresh Token
- **📦 插件管理** - 完整的插件生命周期管理（提交、审核、发布、下架、删除）
- **🏷️ 分类管理** - 插件分类浏览和管理，支持自定义分类
- **✅ 审批工作流** - 多级审批流程，支持批准、驳回、需要修改等操作
- **👨‍💼 管理后台** - 管理员可进行用户、插件、分类、审批者等全方位管理
- **📝 审计日志** - 记录关键操作便于追踪和合规
- **📊 数据统计** - 平台数据统计和可视化展示
- **🌐 响应式设计** - 支持桌面和移动设备访问
- **🔍 搜索筛选** - 插件搜索、分类筛选、排序功能
- **🖼️ 头像代理缓存** - 自动缓存 GitHub 头像，加速加载并减少源站请求
- **🌍 中英双语** - 前端国际化支持，可切换中文/英文界面
- **🔄 GitHub 数据同步** - 支持同步插件 Stars、Forks 等 GitHub 元数据

## 🏗️ 项目架构

```
.
├── backend_py/               # Python + Flask 后端 API
│   ├── app/                  # 应用主目录
│   │   ├── models/           # 数据库模型 (User, Plugin, Category, Review, AuditLog, AvatarCache)
│   │   ├── routes/           # API 路由 (auth, plugins, developer, reviewer, admin, users, avatar)
│   │   ├── services/         # 业务逻辑层 (含 avatar_service)
│   │   └── utils/            # 工具函数 (decorators)
│   ├── config/               # 配置文件
│   ├── migrations/           # 数据库迁移文件
│   ├── requirements.txt      # Python 依赖
│   ├── .env.example          # 环境变量示例
│   ├── wsgi.py               # WSGI 入口
│   ├── update_plugins_github_data.py  # GitHub 数据同步脚本
│   ├── API.md                # 详细 API 文档
│   ├── FRONTEND_INTEGRATION.md # 前端集成指南
│   └── README.md             # 后端说明文档
│
└── frontend/                 # 纯前端 HTML/CSS/JS
    ├── index.html            # 首页/插件列表
    ├── store.html            # 插件商店/详情
    ├── login.html            # 登录页面
    ├── callback.html         # GitHub OAuth 回调
    ├── developer.html        # 开发者中心
    ├── submit-plugin.html    # 提交插件
    ├── my-plugins.html       # 我的插件管理
    ├── admin.html            # 管理后台首页
    ├── admin-users.html      # 用户管理
    ├── admin-plugins.html    # 插件管理
    ├── admin-categories.html # 分类管理
    ├── admin-reviewers.html  # 审批者管理
    ├── admin-stats.html      # 统计数据
    ├── review-plugins.html   # 插件审批
    ├── plugin-detail.html    # 插件详情页
    ├── author.html           # 作者主页
    ├── contributors.html     # 贡献者页面
    ├── privacy.html          # 隐私政策
    ├── terms.html            # 使用条款
    ├── i18n.js               # 国际化模块
    ├── app.js                # 前端主逻辑
    └── styles.css            # 样式文件
```

## 🛠️ 技术栈

### 后端
| 技术 | 说明 |
|------|------|
| [Flask](https://flask.palletsprojects.com/) | Python Web 框架 |
| [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) | ORM 数据库操作 |
| [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/) | JWT 认证 |
| [Flask-Migrate](https://flask-migrate.readthedocs.io/) | 数据库迁移 |
| [Flask-CORS](https://flask-cors.readthedocs.io/) | 跨域支持 |
| [PyMySQL](https://pypi.org/project/PyMySQL/) | MySQL 驱动 |
| [GitHub OAuth](https://docs.github.com/en/developers/apps) | 第三方登录 |

### 前端
| 技术 | 说明 |
|------|------|
| HTML5 + CSS3 + JavaScript (ES6+) | 原生前端技术栈 |
| Fetch API | 原生 HTTP 请求 |
| 响应式设计 | 支持多端访问 |

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+
- GitHub OAuth App

### 1. 克隆项目

```bash
git clone https://github.com/Qixuan112/cjsd1.git
cd plugin-marketplace
```

### 2. 配置后端

```bash
cd backend_py

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写数据库和 GitHub OAuth 配置
```

### 3. 配置数据库

```sql
CREATE DATABASE plugin_marketplace CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 初始化数据库

```bash
# 初始化迁移
flask db init

# 创建迁移脚本
flask db migrate -m "Initial migration"

# 执行迁移
flask db upgrade
```

### 5. 启动后端服务

```bash
# Windows
set FLASK_APP=app
set FLASK_ENV=development
flask run

# macOS/Linux
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

后端服务将运行在 `http://localhost:5000`

### 6. 启动前端

前端是纯静态文件，可以使用任意静态服务器：

```bash
cd frontend

# 使用 Python 简单 HTTP 服务器
python -m http.server 8080

# 或使用 Node.js 的 http-server（需安装）
npx http-server -p 8080
```

访问 `http://localhost:8080` 即可使用。

## ⚙️ 环境变量配置

编辑 `backend_py/.env` 文件：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://用户名:密码@localhost:3306/plugin_marketplace

# JWT 密钥（生产环境请使用强密钥）
JWT_SECRET_KEY=your-secret-key

# GitHub OAuth 配置
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# 可选配置
FLASK_ENV=development
FLASK_PORT=5000
CORS_ORIGINS=*
LOG_LEVEL=INFO
```

## 📚 文档

| 文档 | 路径 | 说明 |
|------|------|------|
| [后端 API 文档](./backend_py/API.md) | `backend_py/API.md` | 详细的 RESTful API 接口文档 |
| [前端集成指南](./backend_py/FRONTEND_INTEGRATION.md) | `backend_py/FRONTEND_INTEGRATION.md` | 前端与后端的集成说明 |
| [后端说明文档](./backend_py/README.md) | `backend_py/README.md` | 后端详细说明和部署指南 |
| [环境变量示例](./backend_py/.env.example) | `backend_py/.env.example` | 环境变量配置模板 |

## 👥 用户角色

| 角色 | 权限 |
|------|------|
| 普通用户 | 浏览插件、提交插件、管理自己的插件 |
| 审批者 | 普通用户权限 + 审核插件 |
| 管理员 | 所有权限 + 系统管理 |

## 🌐 API 概览

| 模块 | 基础路径 | 说明 | 权限 |
|------|----------|------|------|
| 认证 | `/api/auth/*` | GitHub OAuth、Token 刷新、当前用户 | 公开 |
| 插件公开 | `/api/plugins/*` | 插件列表、详情、搜索 | 公开 |
| 分类公开 | `/api/categories/*` | 分类列表、详情 | 公开 |
| 开发者 | `/api/developer/*` | 提交插件、我的插件、更新插件 | 登录用户 |
| 审批者 | `/api/reviewer/*` | 审批队列、审批操作、审批历史 | Reviewer+ |
| 管理端 | `/api/admin/*` | 用户/插件/分类/审批者管理、审计日志、统计 | Admin |
| 用户端 | `/api/users/*` | 个人信息、修改信息 | 登录用户 |
| 头像代理 | `/api/avatar/*` | 头像缓存、代理、统计 | 公开 |

## 📸 页面预览

| 页面 | 路径 | 功能描述 |
|------|------|----------|
| **首页** | `index.html` | 插件浏览、搜索、分类筛选 |
| **插件商店** | `store.html` | 插件展示和推荐 |
| **插件详情** | `plugin-detail.html` | 查看插件详细信息、版本、README |
| **登录页** | `login.html` | GitHub OAuth 登录入口 |
| **开发者中心** | `developer.html` | 开发者仪表盘和统计 |
| **提交插件** | `submit-plugin.html` | 新插件提交表单 |
| **我的插件** | `my-plugins.html` | 管理自己提交的插件 |
| **插件审批** | `review-plugins.html` | 审批者审核插件 (Reviewer+) |
| **管理后台** | `admin.html` | 管理员仪表盘 (Admin) |
| **用户管理** | `admin-users.html` | 管理系统用户 (Admin) |
| **插件管理** | `admin-plugins.html` | 管理所有插件 (Admin) |
| **分类管理** | `admin-categories.html` | 管理插件分类 (Admin) |
| **审批者管理** | `admin-reviewers.html` | 设置审批者 (Admin) |
| **统计报表** | `admin-stats.html` | 查看平台统计数据 (Admin) |
| **OAuth 回调** | `callback.html` | GitHub 登录回调处理 |
| **作者主页** | `author.html` | 查看作者信息和插件列表 |
| **贡献者** | `contributors.html` | 开源贡献者和社区支持者 |
| **隐私政策** | `privacy.html` | 隐私政策说明 |
| **使用条款** | `terms.html` | 服务使用条款 |

## 🔒 安全说明

- ⚠️ 生产环境请务必修改默认的 JWT 密钥
- 🔒 使用 HTTPS 部署
- 🗝️ 妥善保管 GitHub OAuth 密钥
- 💾 定期备份数据库

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/xxx`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送到分支：`git push origin feature/xxx`
5. 提交 Pull Request

## 📄 许可证

本项目采用 [AGPL-3.0](./LICENSE) 开源许可证。

---

<p align="center">
  如有问题或建议，欢迎提交 <a href="https://github.com/Qixuan112/cjsd1/issues">Issue</a> 或 <a href="https://github.com/Qixuan112/cjsd1/pulls">Pull Request</a>
</p>

<p align="center">
  ⭐ Star 这个项目，如果你发现它有帮助！
</p>
