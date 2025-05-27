# -*- coding: utf-8 -*-
"""AIML规则管理和对话接口"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.aiml_service import AIMLService
from ..services.aiml_manager import AIMLManager
from ..models import db, ChatSession, Message, User
import logging

bp = Blueprint('aiml', __name__)
logger = logging.getLogger(__name__)

# 全局AIML服务实例
aiml_service = None

def get_aiml_service():
    """获取AIML服务实例，如果未初始化则初始化"""
    global aiml_service
    if aiml_service is None:
        aiml_service = AIMLService()
        logger.info("AIML服务已初始化")
    return aiml_service

@bp.route('/chat', methods=['POST'])
def chat():
    """AIML对话接口"""
    data = request.get_json()
    
    if 'message' not in data:
        return jsonify({'error': '缺少输入内容'}), 400
    
    user_input = data['message']
    session_id = data.get('session_id')
    
    # 获取AIML响应
    service = get_aiml_service()
    response = service.get_response(user_input, session_id)
    
    # 保存对话历史
    if session_id:
        try:
            # 保存用户消息
            user_message = Message(
                session_id=session_id,
                role='user',
                content=user_input
            )
            db.session.add(user_message)
            
            # 保存助手回复
            assistant_message = Message(
                session_id=session_id,
                role='assistant',
                content=response
            )
            db.session.add(assistant_message)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"保存对话历史失败: {str(e)}")
            db.session.rollback()
    
    return jsonify({
        'response': response,
        'session_id': session_id
    }), 200

@bp.route('/files', methods=['GET'])
@jwt_required()
def get_files():
    """获取所有AIML文件"""
    manager = AIMLManager()
    files = manager.get_all_files()
    
    return jsonify(files), 200

@bp.route('/files/<filename>', methods=['GET'])
@jwt_required()
def get_file_content(filename):
    """获取AIML文件内容"""
    manager = AIMLManager()
    content = manager.get_file_content(filename)
    
    if content is None:
        return jsonify({'error': '文件不存在或无法读取'}), 404
    
    return jsonify({
        'filename': filename,
        'content': content
    }), 200

@bp.route('/files', methods=['POST'])
@jwt_required()
def create_file():
    """创建新的AIML文件"""
    data = request.get_json()
    
    if 'filename' not in data:
        return jsonify({'error': '缺少文件名'}), 400
    
    filename = data['filename']
    content = data.get('content', '')
    
    manager = AIMLManager()
    result = manager.create_file(filename, content)
    
    if not result:
        return jsonify({'error': '文件创建失败，可能文件已存在'}), 400
    
    # 重新初始化AIML服务，加载新文件
    get_aiml_service()  # 确保服务已初始化
    global aiml_service
    aiml_service = AIMLService()  # 重新加载
    
    return jsonify({
        'message': '文件创建成功',
        'filename': filename
    }), 201

@bp.route('/files/<filename>', methods=['PUT'])
@jwt_required()
def update_file(filename):
    """更新AIML文件内容"""
    data = request.get_json()
    
    if 'content' not in data:
        return jsonify({'error': '缺少文件内容'}), 400
    
    content = data['content']
    
    manager = AIMLManager()
    result = manager.save_file_content(filename, content)
    
    if not result:
        return jsonify({'error': '文件保存失败，可能XML格式不正确'}), 400
    
    # 重新初始化AIML服务，加载更新后的文件
    get_aiml_service()  # 确保服务已初始化
    global aiml_service
    aiml_service = AIMLService()  # 重新加载
    
    return jsonify({
        'message': '文件更新成功',
        'filename': filename
    }), 200

@bp.route('/files/<filename>', methods=['DELETE'])
@jwt_required()
def delete_file(filename):
    """删除AIML文件"""
    manager = AIMLManager()
    result = manager.delete_file(filename)
    
    if not result:
        return jsonify({'error': '文件删除失败，可能文件不存在'}), 404
    
    # 重新初始化AIML服务
    get_aiml_service()  # 确保服务已初始化
    global aiml_service
    aiml_service = AIMLService()  # 重新加载
    
    return jsonify({
        'message': '文件删除成功',
        'filename': filename
    }), 200

@bp.route('/patterns/<filename>', methods=['GET'])
@jwt_required()
def get_patterns(filename):
    """获取AIML文件中的所有模式"""
    manager = AIMLManager()
    patterns = manager.extract_patterns(filename)
    
    if patterns is None:
        return jsonify({'error': '文件不存在或无法读取'}), 404
    
    return jsonify(patterns), 200

@bp.route('/patterns', methods=['POST'])
@jwt_required()
def add_pattern():
    """添加新的AIML模式"""
    data = request.get_json()
    
    if 'filename' not in data or 'pattern' not in data or 'template' not in data:
        return jsonify({'error': '缺少必要参数'}), 400
    
    filename = data['filename']
    pattern = data['pattern']
    template = data['template']
    
    manager = AIMLManager()
    result = manager.add_pattern(filename, pattern, template)
    
    if not result:
        return jsonify({'error': '添加模式失败，可能文件不存在'}), 400
    
    # 向AIML服务添加新模式
    service = get_aiml_service()
    service.learn_pattern(pattern, template)
    
    return jsonify({
        'message': '模式添加成功',
        'filename': filename,
        'pattern': pattern
    }), 201

@bp.route('/import', methods=['POST'])
@jwt_required()
def import_patterns():
    """批量导入AIML模式"""
    data = request.get_json()
    
    if 'data' not in data or not isinstance(data['data'], list):
        return jsonify({'error': '缺少数据或格式不正确'}), 400
    
    manager = AIMLManager()
    result = manager.import_categories(data['data'])
    
    # 重新初始化AIML服务
    get_aiml_service()  # 确保服务已初始化
    global aiml_service
    aiml_service = AIMLService()  # 重新加载
    
    return jsonify({
        'message': f'导入完成，成功{result["success"]}条，失败{result["failed"]}条',
        'result': result
    }), 200

@bp.route('/learn', methods=['POST'])
@jwt_required()
def learn_pattern():
    """学习新的问答模式"""
    service = get_aiml_service()
    
    data = request.get_json()
    
    if 'pattern' not in data or 'template' not in data:
        return jsonify({'error': '缺少必要参数'}), 400
    
    pattern = data['pattern']
    template = data['template']
    filename = data.get('filename', 'learned.aiml')
    
    # 添加到文件
    manager = AIMLManager()
    file_result = manager.add_pattern(filename, pattern, template)
    
    # 让内核学习
    kernel_result = service.learn_pattern(pattern, template)
    
    if not file_result or not kernel_result:
        return jsonify({'error': '学习模式失败'}), 400
    
    return jsonify({
        'message': '模式学习成功',
        'pattern': pattern,
        'filename': filename
    }), 201 