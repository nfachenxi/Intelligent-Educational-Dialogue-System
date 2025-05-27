# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, ChatSession, Message, User
from ..services.aiml_service import AIMLService
import logging

bp = Blueprint('chat', __name__)
logger = logging.getLogger(__name__)

# 全局AIML服务实例
aiml_service = None

def get_aiml_service():
    """获取AIML服务实例，如果未初始化则初始化"""
    global aiml_service
    if aiml_service is None:
        aiml_service = AIMLService()
        logger.info("聊天模块AIML服务已初始化")
    return aiml_service

@bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    """获取用户的所有会话"""
    user_id = get_jwt_identity()
    sessions = ChatSession.query.filter_by(user_id=user_id).all()
    
    return jsonify([
        {
            'id': session.id,
            'name': session.name,
            'created_at': session.created_at.isoformat(),
            'updated_at': session.updated_at.isoformat(),
            'is_archived': session.is_archived
        } for session in sessions
    ])

@bp.route('/sessions', methods=['POST'])
@jwt_required()
def create_session():
    """创建新的聊天会话"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    session = ChatSession(
        name=data.get('name', f'会话 {datetime.now().strftime("%Y-%m-%d %H:%M")}'),
        user_id=user_id
    )
    
    db.session.add(session)
    db.session.commit()
    
    return jsonify({
        'message': '会话创建成功',
        'session_id': session.id
    }), 201

@bp.route('/sessions/<int:session_id>', methods=['GET'])
@jwt_required()
def get_session(session_id):
    """获取指定会话及其消息"""
    user_id = get_jwt_identity()
    session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first_or_404()
    messages = Message.query.filter_by(session_id=session_id).order_by(Message.created_at.asc()).all()
    
    return jsonify({
        'id': session.id,
        'name': session.name,
        'created_at': session.created_at.isoformat(),
        'updated_at': session.updated_at.isoformat(),
        'is_archived': session.is_archived,
        'messages': [
            {
                'id': msg.id,
                'role': msg.role,
                'content': msg.content,
                'created_at': msg.created_at.isoformat()
            } for msg in messages
        ]
    })

@bp.route('/sessions/<int:session_id>', methods=['PUT'])
@jwt_required()
def update_session(session_id):
    """更新会话信息"""
    user_id = get_jwt_identity()
    session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first_or_404()
    data = request.get_json()
    
    if 'name' in data:
        session.name = data['name']
        
    db.session.commit()
    
    return jsonify({
        'id': session.id,
        'name': session.name,
        'created_at': session.created_at.isoformat(),
        'updated_at': session.updated_at.isoformat(),
        'is_archived': session.is_archived
    })

@bp.route('/sessions/<int:session_id>/archive', methods=['POST'])
@jwt_required()
def archive_session(session_id):
    """归档会话"""
    user_id = get_jwt_identity()
    session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first_or_404()
    
    session.is_archived = True
    db.session.commit()
    
    return jsonify({
        'id': session.id,
        'name': session.name,
        'archived': session.is_archived
    })

@bp.route('/sessions/<int:session_id>/messages', methods=['POST'])
@jwt_required()
def send_message(session_id):
    """发送消息"""
    user_id = get_jwt_identity()
    session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first_or_404()
    data = request.get_json()
    
    # 保存用户消息
    message = Message(
        session_id=session_id,
        role='user',
        content=data.get('content', '')
    )
    db.session.add(message)
    db.session.commit()
    
    return jsonify({
        'message_id': message.id,
        'session_id': session_id,
        'status': 'sent'
    }), 201 