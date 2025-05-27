"""
扩展模块，用于存放Flask扩展实例
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# 数据库实例
db = SQLAlchemy()

# 数据库迁移实例
migrate = Migrate()

# CORS实例
cors = CORS() 