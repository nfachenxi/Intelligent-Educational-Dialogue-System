# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import os
import logging

# 创建蓝图
bp = Blueprint('main', __name__)

# 创建日志记录器
logger = logging.getLogger(__name__)

@bp.route('/')
def index():
    """首页"""
    return render_template('index.html')

@bp.route('/login')
def login():
    """登录页面"""
    # 简单实现，实际应用中应有更完善的登录逻辑
    return render_template('login.html')

@bp.route('/register')
def register():
    """注册页面"""
    # 简单实现，实际应用中应有更完善的注册逻辑
    return render_template('register.html')

@bp.route('/chat')
def chat():
    """聊天主页"""
    return render_template('chat.html')

@bp.route('/aiml')
def aiml_chat():
    """AIML规则对话页面"""
    return render_template('aiml_chat.html')

@bp.route('/gpt2-chat')
def gpt2_chat():
    """GPT-2生成对话页面"""
    return render_template('gpt2_chat.html')

@bp.route('/admin/models')
@jwt_required(optional=True)
def model_management():
    """模型管理页面"""
    # 检查用户权限
    current_user = get_jwt_identity()
    if not current_user:
        # 未登录用户重定向到登录页面
        return redirect(url_for('main.login'))
        
    return render_template('model_management.html')

@bp.route('/mock-login', methods=['POST'])
def mock_login():
    """模拟登录接口，仅用于开发测试"""
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    # 开发环境测试用户
    if username == 'test' and password == 'test123':
        access_token = create_access_token(identity='1')  # 用户ID为1
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': 1,
                'username': 'test',
                'role': 'admin'
            }
        })
    
    return jsonify({'error': '用户名或密码错误'}), 401

@bp.route('/info')
def info():
    """系统信息页面"""
    return render_template('info.html')

@bp.route('/api/chat', methods=['POST'])
def chat_api():
    """处理聊天请求的端点"""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    # TODO: 实现对话处理逻辑
    return jsonify({
        'response': '这是一个测试响应',
        'status': 'success'
    }) 