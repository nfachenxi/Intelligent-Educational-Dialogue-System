# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .extensions import db, migrate, cors
from .routes import auth, chat, aiml, gpt2, main
import logging

def create_app(config=None):
    app = Flask(__name__)
    CORS(app)

    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # 请在生产环境中使用安全的密钥
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt = JWTManager(app)
    
    # 注册蓝图
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(chat.bp, url_prefix='/chat')
    app.register_blueprint(aiml.bp, url_prefix='/aiml')
    app.register_blueprint(gpt2.bp, url_prefix='/gpt2')
    app.register_blueprint(main.bp)  # 主路由不设置前缀
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app 