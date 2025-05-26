# -*- coding: utf-8 -*-
import os
from datetime import timedelta

# 获取当前文件所在目录的父目录（项目根目录）
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 基础配置
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'

# 数据库配置
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data', 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT配置
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

# AIML配置
AIML_PATH = os.path.join(basedir, 'data', 'aiml')

# 模型配置
MODEL_PATH = os.path.join(basedir, 'data', 'models')

# 知识图谱配置
KNOWLEDGE_GRAPH_PATH = os.path.join(basedir, 'data', 'knowledge_graph') 