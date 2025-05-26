# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models import init_db

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 配置加载
    app.config.from_object('config.default')
    
    # 初始化数据库
    init_db(app)
    
    # 初始化JWT
    jwt = JWTManager(app)
    
    # 注册蓝图
    from app.routes import main, auth, chat
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(chat.bp, url_prefix='/chat')

    return app 