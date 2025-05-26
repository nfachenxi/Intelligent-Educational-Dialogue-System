# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request

bp = Blueprint('main', __name__)

@bp.route('/api/chat', methods=['POST'])
def chat():
    """处理聊天请求的端点"""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    # TODO: 实现对话处理逻辑
    return jsonify({
        'response': '这是一个测试响应',
        'status': 'success'
    }) 