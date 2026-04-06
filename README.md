# 🔌 插件市场 (Plugin Marketplace)

<p align="center">
  <b>一个功能完善的插件市场系统，支持插件的提交、审核、发布和管理。</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Flask-2.0+-green.svg" alt="Flask 2.0+">
  <img src="https://img.shields.io/badge/MySQL-5.7+-orange.svg" alt="MySQL 5.7+">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
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

- **🔐 用户认证** - 基于 GitHub OAuth 的登录系统，JWT 身份验证
- **📦 插件管理** - 完整的插件生命周期管理（提交、审核、发布、下架）
- **✅ 审批工作流** - 审批者对插件进行审核操作
- **👨‍💼 管理后台** - 管理员可进行用户、插件、分类、审批者等管理
- **📝 审计日志** - 记录关键操作便于追踪
- **📱 响应式设计** - 支持桌面和移动设备访问

## 🏗️ 项目架构

```
.
├── backend_py/          # Python + Flask 后端 API
│   ├── app/             # 应用主目录
│   │   ├── models/      # 数据库模型
│   │   ├── routes/      # API 路由
│   │   ├── services/    # 业务逻辑
│   │   └── utils/       # 工具函数
│   ├── config/          # 配置文件
│   ├── requirements.txt # Python 依赖
│   ├── API.md           # 详细 API 文档
│   └── README.md        # 后端说明文档
│
└── frontend/            # 纯前端 HTML/CSS/JS
    ├── index.html       # 首页/插件列表
    ├── login.html       # 登录页面
    ├── store.html       # 插件详情
    ├── developer.html   # 开发者中心
    ├── admin.html       # 管理后台
    ├── app.js           # 前端逻辑
    └── styles.css       # 样式文件
```

## 🛠️ 技术栈

### 后端
| 技术 | 说明 |
|------|------|
| [Flask](https://flask.palletsprojects.com/) | Python Web 框架 |
| [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) | ORM 数据库操作 |
| [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/) | JWT 认证 |
| [MySQL](https://www.mysql.com/) | 数据库 |
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
git clone https://github.com/your-username/plugin-marketplace.git
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

| 文档 | 说明 |
|------|------|
| [后端 API 文档](./backend_py/API.md) | 详细的 RESTful API 接口文档 |
| [前端集成指南](./backend_py/FRONTEND_INTEGRATION.md) | 前端与后端的集成说明 |
| [后端说明文档](./backend_py/README.md) | 后端的详细说明 |

## 👥 用户角色

| 角色 | 权限 |
|------|------|
| 普通用户 | 浏览插件、提交插件、管理自己的插件 |
| 审批者 | 普通用户权限 + 审核插件 |
| 管理员 | 所有权限 + 系统管理 |

## 🌐 API 概览

| 模块 | 基础路径 | 说明 |
|------|----------|------|
| 认证 | `/api/auth/*` | GitHub OAuth、Token 刷新 |
| 公开端 | `/api/plugins`, `/api/categories` | 插件列表、详情、分类 |
| 开发者端 | `/api/developer/*` | 提交插件、我的插件 |
| 审批者端 | `/api/reviewer/*` | 审批队列、审批操作 |
| 管理端 | `/api/admin/*` | 用户、插件、分类管理 |
| 用户端 | `/api/user/*` | 个人信息 |

## 📸 页面预览

| 页面 | 功能描述 |
|------|----------|
| **首页** | 插件浏览和搜索 |
| **登录页** | GitHub OAuth 登录 |
| **插件详情** | 查看插件信息和安装 |
| **开发者中心** | 提交和管理插件 |
| **管理后台** | 系统管理和审批 |

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

本项目采用 [MIT License](./LICENSE) 开源许可证。

---

<p align="center">
  如有问题或建议，欢迎提交 <a href="https://github.com/your-username/plugin-marketplace/issues">Issue</a> 或 <a href="https://github.com/your-username/plugin-marketplace/pulls">Pull Request</a>
</p>

<p align="center">
  ⭐ Star 这个项目，如果你发现它有帮助！
</p>
