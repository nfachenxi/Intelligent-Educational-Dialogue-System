# -*- coding: utf-8 -*-
"""AIML规则管理和对话接口"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.aiml_service import AIMLService
from ..services.aiml_manager import AIMLManager
from ..models import db, ChatHistory

bp = Blueprint('aiml', __name__)

# 全局AIML服务实例
aiml_service = None

@bp.before_app_request
def initialize_aiml_service():
    """初始化AIML服务"""
    global aiml_service
    if aiml_service is None:
        aiml_service = AIMLService()

@bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    """AIML对话接口"""
    global aiml_service
    if aiml_service is None:
        aiml_service = AIMLService()
    
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if 'message' not in data:
        return jsonify({'error': '缺少消息内容'}), 400
    
    message = data['message']
    session_id = data.get('session_id')
    
    # 获取AIML响应
    response = aiml_service.get_response(message, session_id)
    
    # 保存对话历史
    if session_id:
        try:
            chat_history = ChatHistory(
                user_id=current_user_id,
                session_id=session_id,
                message=message,
                response=response,
                message_type='text',
                source='aiml'
            )
            db.session.add(chat_history)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"保存对话历史失败: {str(e)}")
            db.session.rollback()
    
    return jsonify({
        'message': message,
        'response': response,
        'source': 'aiml'
    }), 200

@bp.route('/files', methods=['GET'])
@jwt_required()
def get_files():
    """获取所有AIML文件"""
    manager = AIMLManager()
    files = manager.get_all_files()
    
    return jsonify({
        'files': files,
        'count': len(files)
    }), 200

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
    categories = data.get('categories', [])
    
    manager = AIMLManager()
    result = manager.create_file(filename, categories)
    
    if not result:
        return jsonify({'error': '文件创建失败，可能文件已存在'}), 400
    
    # 重新初始化AIML服务，加载新文件
    global aiml_service
    aiml_service = AIMLService()
    
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
    global aiml_service
    aiml_service = AIMLService()
    
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
    global aiml_service
    aiml_service = AIMLService()
    
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
    
    return jsonify({
        'filename': filename,
        'patterns': [{'pattern': p, 'template': t} for p, t in patterns],
        'count': len(patterns)
    }), 200

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
    global aiml_service
    if aiml_service:
        aiml_service.learn_pattern(pattern, template)
    
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
    global aiml_service
    aiml_service = AIMLService()
    
    return jsonify({
        'message': f'导入完成，成功{result["success"]}条，失败{result["failed"]}条',
        'result': result
    }), 200

@bp.route('/learn', methods=['POST'])
@jwt_required()
def learn_pattern():
    """学习新的问答模式"""
    global aiml_service
    if aiml_service is None:
        aiml_service = AIMLService()
    
    data = request.get_json()
    
    if 'pattern' not in data or 'template' not in data:
        return jsonify({'error': '缺少必要参数'}), 400
    
    pattern = data['pattern']
    template = data['template']
    
    result = aiml_service.learn_pattern(pattern, template)
    
    if not result:
        return jsonify({'error': '学习模式失败'}), 400
    
    return jsonify({
        'message': '模式学习成功',
        'pattern': pattern
    }), 201 