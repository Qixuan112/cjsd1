"""
App 包初始化模块

Flask 应用工厂和扩展初始化
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv

from config.config import config

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # 配置 CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('CORS_ORIGINS', '*'),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 注册模型（确保 SQLAlchemy 能识别所有模型）
    from app.models import User, Category, Plugin, Review, AuditLog
    
    # 注册蓝图
    from app.routes import auth, user, plugins, categories, developer, reviewer, admin
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(user.bp, url_prefix='/api/users')
    app.register_blueprint(plugins.bp, url_prefix='/api/plugins')
    app.register_blueprint(categories.bp, url_prefix='/api/categories')
    app.register_blueprint(developer.bp, url_prefix='/api/developer')
    app.register_blueprint(reviewer.bp, url_prefix='/api/reviewer')
    app.register_blueprint(admin.bp, url_prefix='/api/admin')
    
    # 健康检查端点
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Service is running'}
    
    return app
