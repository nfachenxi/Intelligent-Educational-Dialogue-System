"""
创建测试用户脚本
"""
import os
import sys
from flask import Flask
from werkzeug.security import generate_password_hash

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extensions import db
from app.models.user import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def create_test_user():
    """创建测试用户"""
    with app.app_context():
        # 检查测试用户是否已存在
        if User.query.filter_by(username='test_user').first():
            print('测试用户已存在')
            return
        
        # 创建测试用户
        user = User(
            username='test_user',
            email='test@example.com',
            role='student'
        )
        user.password_hash = generate_password_hash('test123')
        
        db.session.add(user)
        db.session.commit()
        print('测试用户创建成功')

if __name__ == '__main__':
    create_test_user() 