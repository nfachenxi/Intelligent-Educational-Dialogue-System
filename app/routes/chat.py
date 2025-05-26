# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, ChatSession, ChatHistory, User
from ..services.aiml_service import AIMLService

bp = Blueprint('chat', __name__)

# 全局AIML服务实例
aiml_service = None

@bp.before_app_request
def initialize_aiml_service():
    """初始化AIML服务"""
    global aiml_service
    if aiml_service is None:
        aiml_service = AIMLService()

@bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    """获取用户的所有会话"""
    current_user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', 'active')
    
    # 查询会话列表
    query = ChatSession.query.filter_by(
        user_id=current_user_id,
        status=status
    ).order_by(ChatSession.updated_at.desc())
    
    # 分页
    pagination = query.paginate(page=page, per_page=per_page)
    sessions = pagination.items
    
    return jsonify({
        'sessions': [session.to_dict() for session in sessions],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@bp.route('/sessions', methods=['POST'])
@jwt_required()
def create_session():
    """创建新会话"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    # 生成会话ID
    session_id = str(uuid.uuid4())
    
    # 创建会话
    session = ChatSession(
        session_id=session_id,
        user_id=current_user_id,
        title=data.get('title', '新会话'),
        max_context_length=data.get('max_context_length', 10),
        language=data.get('language', 'zh-CN')
    )
    
    try:
        db.session.add(session)
        db.session.commit()
        return jsonify({
            'message': '会话创建成功',
            'session': session.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '会话创建失败'}), 500

@bp.route('/sessions/<session_id>', methods=['GET'])
@jwt_required()
def get_session(session_id):
    """获取会话详情"""
    current_user_id = int(get_jwt_identity())
    
    # 查询会话
    session = ChatSession.query.filter_by(
        session_id=session_id,
        user_id=current_user_id
    ).first()
    
    if not session:
        return jsonify({'error': '会话不存在'}), 404
    
    # 获取最近的消息
    messages = session.get_context()
    
    return jsonify({
        'session': session.to_dict(),
        'messages': [msg.to_dict() for msg in messages]
    }), 200

@bp.route('/sessions/<session_id>/messages', methods=['POST'])
@jwt_required()
def send_message(session_id):
    """发送消息"""
    global aiml_service
    if aiml_service is None:
        aiml_service = AIMLService()
        
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if 'message' not in data:
        return jsonify({'error': '缺少消息内容'}), 400
    
    # 查询会话
    session = ChatSession.query.filter_by(
        session_id=session_id,
        user_id=current_user_id,
        status='active'
    ).first()
    
    if not session:
        return jsonify({'error': '会话不存在或已结束'}), 404
    
    try:
        message_text = data['message']
        message_type = data.get('message_type', 'text')
        
        # 获取AIML响应
        response = aiml_service.get_response(message_text, session_id)
        
        # 创建新消息
        message = ChatHistory(
            user_id=current_user_id,
            session_id=session_id,
            message=message_text,
            response=response,
            message_type=message_type,
            source='aiml'  # 标记来源为AIML
        )
        db.session.add(message)
        
        # 更新会话信息
        session.update_last_message()
        
        db.session.commit()
        
        return jsonify({
            'message': message.to_dict(),
            'session': session.to_dict()
        }), 201
    except Exception as e:
        current_app.logger.error(f"消息发送失败: {str(e)}")
        db.session.rollback()
        return jsonify({'error': '消息发送失败'}), 500

@bp.route('/sessions/<session_id>', methods=['PUT'])
@jwt_required()
def update_session(session_id):
    """更新会话信息"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    # 查询会话
    session = ChatSession.query.filter_by(
        session_id=session_id,
        user_id=current_user_id
    ).first()
    
    if not session:
        return jsonify({'error': '会话不存在'}), 404
    
    try:
        # 更新可修改的字段
        if 'title' in data:
            session.title = data['title']
        if 'max_context_length' in data:
            session.max_context_length = data['max_context_length']
        if 'language' in data:
            session.language = data['language']
        
        db.session.commit()
        return jsonify({
            'message': '会话更新成功',
            'session': session.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '会话更新失败'}), 500

@bp.route('/sessions/<session_id>', methods=['DELETE'])
@jwt_required()
def delete_session(session_id):
    """删除会话（软删除）"""
    current_user_id = int(get_jwt_identity())
    
    # 查询会话
    session = ChatSession.query.filter_by(
        session_id=session_id,
        user_id=current_user_id
    ).first()
    
    if not session:
        return jsonify({'error': '会话不存在'}), 404
    
    try:
        session.delete()
        db.session.commit()
        return jsonify({'message': '会话删除成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '会话删除失败'}), 500

@bp.route('/sessions/<session_id>/archive', methods=['POST'])
@jwt_required()
def archive_session(session_id):
    """归档会话"""
    current_user_id = int(get_jwt_identity())
    
    # 查询会话
    session = ChatSession.query.filter_by(
        session_id=session_id,
        user_id=current_user_id
    ).first()
    
    if not session:
        return jsonify({'error': '会话不存在'}), 404
    
    try:
        session.archive()
        db.session.commit()
        return jsonify({
            'message': '会话归档成功',
            'session': session.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '会话归档失败'}), 500 