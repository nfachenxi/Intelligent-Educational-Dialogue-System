# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import datetime
from ..models import db, User
from ..utils.validators import validate_email

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    """用户注册接口"""
    data = request.get_json()
    
    # 验证必要字段
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'error': '缺少必要字段'}), 400
    
    # 验证邮箱格式
    if not validate_email(data['email']):
        return jsonify({'error': '邮箱格式不正确'}), 400
    
    # 检查用户名和邮箱是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '邮箱已被注册'}), 400
    
    # 创建新用户
    user = User(
        username=data['username'],
        email=data['email'],
        role=data.get('role', 'student')
    )
    user.password = data['password']
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message': '注册成功',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    """用户登录接口"""
    data = request.get_json()
    
    # 验证必要字段
    if not all(k in data for k in ('username', 'password')):
        return jsonify({'error': '缺少必要字段'}), 400
    
    # 查找用户
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.verify_password(data['password']):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    if not user.is_active:
        return jsonify({'error': '账号已被禁用'}), 403
    
    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # 生成访问令牌和刷新令牌
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        'message': '登录成功',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@bp.route('/user', methods=['GET'])
@jwt_required()
def get_user_info():
    """获取当前用户信息"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at.isoformat()
    }), 200

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """刷新访问令牌"""
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token}), 200 