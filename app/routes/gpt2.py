from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.gpt2 import GPT2Generator
from ..models import db, ChatSession, Message
import logging
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename

# 创建日志记录器
logger = logging.getLogger(__name__)

bp = Blueprint('gpt2', __name__)
generator = None

# 模型缓存目录的基本路径，不依赖current_app
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'models'))
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR, exist_ok=True)

def get_model_dir():
    """获取模型目录路径，在应用上下文中使用"""
    if current_app:
        return os.path.join(current_app.root_path, '..', 'data', 'models')
    return BASE_DIR

def init_gpt2(use_mock=True):
    """初始化GPT-2模型"""
    global generator
    try:
        generator = GPT2Generator(use_mock=use_mock)
        logger.info("GPT-2模型初始化成功")
    except Exception as e:
        logger.error(f"GPT-2模型初始化失败: {str(e)}")
        # 失败时尝试使用模拟模式
        generator = GPT2Generator(use_mock=True)
        logger.info("使用模拟模式初始化GPT-2模型")

@bp.route('/status', methods=['GET'])
def status():
    """获取GPT-2模型状态"""
    global generator
    if not generator:
        try:
            init_gpt2()
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'模型初始化失败: {str(e)}',
                'mode': 'mock'
            }), 500
    
    return jsonify({
        'status': 'ok',
        'mode': 'mock' if generator.use_mock else 'normal',
        'model_name': generator.model_name if hasattr(generator, 'model_name') else 'unknown'
    })

@bp.route('/chat', methods=['POST'])
def chat():
    """GPT-2对话接口"""
    try:
        data = request.get_json()
        message = data.get('message')
        session_id = data.get('session_id')
        
        if not message:
            return jsonify({'error': '消息不能为空'}), 400
            
        # 获取会话上下文
        context = []
        if session_id:
            session = ChatSession.query.get(session_id)
            if session:
                messages = Message.query.filter_by(session_id=session_id).order_by(Message.created_at.asc()).all()
                for msg in messages[-6:]:  # 获取最近3轮对话（6条消息）
                    context.append({
                        'role': 'user' if msg.role == 'user' else 'assistant',
                        'content': msg.content
                    })
        
        # 生成回复
        if not generator:
            init_gpt2()
        response = generator.chat(message, context)
        
        # 保存对话记录
        if session_id:
            # 保存用户消息
            user_message = Message(
                session_id=session_id,
                role='user',
                content=message
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
        
        return jsonify({
            'response': response,
            'session_id': session_id
        })
        
    except Exception as e:
        logger.error(f"GPT-2对话失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/generate', methods=['POST'])
@jwt_required()
def generate():
    """GPT-2文本生成接口"""
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        max_length = data.get('max_length', 100)
        num_sequences = data.get('num_sequences', 1)
        temperature = data.get('temperature', 0.7)
        top_k = data.get('top_k', 50)
        top_p = data.get('top_p', 0.9)
        
        if not prompt:
            return jsonify({'error': '提示文本不能为空'}), 400
            
        if not generator:
            init_gpt2()
            
        texts = generator.generate(
            prompt=prompt,
            max_length=max_length,
            num_return_sequences=num_sequences,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p
        )
        
        return jsonify({
            'generated_texts': texts
        })
        
    except Exception as e:
        logger.error(f"GPT-2生成失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/finetune', methods=['POST'])
@jwt_required()
def finetune():
    """微调GPT-2模型"""
    try:
        # 检查用户权限
        user_id = get_jwt_identity()
        # TODO: 添加权限检查
        
        # 获取微调参数
        data = request.get_json()
        train_data_path = data.get('train_data_path')
        num_epochs = data.get('num_epochs', 3)
        
        if not train_data_path:
            return jsonify({'error': '训练数据路径不能为空'}), 400
            
        # 检查训练数据是否存在
        if not os.path.exists(train_data_path):
            return jsonify({'error': '训练数据不存在'}), 404
            
        # 创建输出目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_dir = get_model_dir()
        output_dir = os.path.join(model_dir, f'finetuned_{timestamp}')
        os.makedirs(output_dir, exist_ok=True)
        
        # 初始化模型（如果未初始化）
        if not generator:
            init_gpt2(use_mock=False)
            
        # 执行微调
        result = generator.fine_tune(
            train_data_path=train_data_path,
            output_dir=output_dir,
            num_epochs=num_epochs
        )
        
        return jsonify({
            'status': 'success',
            'message': result,
            'output_dir': output_dir
        })
        
    except Exception as e:
        logger.error(f"微调GPT-2模型失败: {str(e)}")
        return jsonify({'error': str(e)}), 500
        
@bp.route('/upload_data', methods=['POST'])
@jwt_required()
def upload_training_data():
    """上传训练数据"""
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
            
        # 检查文件类型
        if not file.filename.endswith(('.txt', '.json', '.csv')):
            return jsonify({'error': '不支持的文件类型，请上传txt、json或csv文件'}), 400
            
        # 保存文件
        filename = secure_filename(file.filename)
        data_dir = os.path.join(current_app.root_path, '..', 'data', 'training_data')
        os.makedirs(data_dir, exist_ok=True)
        
        file_path = os.path.join(data_dir, filename)
        file.save(file_path)
        
        return jsonify({
            'status': 'success',
            'message': '文件上传成功',
            'file_path': file_path
        })
        
    except Exception as e:
        logger.error(f"上传训练数据失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/models', methods=['GET'])
@jwt_required()
def list_models():
    """列出可用的模型"""
    try:
        models = []
        # 获取模型目录
        model_dir = get_model_dir()
        
        # 检查模型目录
        if os.path.exists(model_dir):
            for item in os.listdir(model_dir):
                item_path = os.path.join(model_dir, item)
                if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, 'config.json')):
                    # 添加到模型列表
                    model_info = {
                        'name': item,
                        'path': item_path,
                        'created': datetime.fromtimestamp(os.path.getctime(item_path)).isoformat()
                    }
                    models.append(model_info)
        
        # 添加默认模型
        models.append({
            'name': 'uer/gpt2-chinese-cluecorpussmall',
            'path': 'huggingface',
            'type': 'pretrained',
            'description': '预训练中文GPT-2模型'
        })
        
        return jsonify({
            'models': models
        })
        
    except Exception as e:
        logger.error(f"获取模型列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/load_model', methods=['POST'])
@jwt_required()
def load_model():
    """加载指定模型"""
    global generator
    try:
        data = request.get_json()
        model_path = data.get('model_path')
        use_mock = data.get('use_mock', False)
        
        if not model_path:
            return jsonify({'error': '模型路径不能为空'}), 400
            
        # 尝试加载模型
        try:
            generator = GPT2Generator(model_name=model_path, use_mock=use_mock)
            logger.info(f"成功加载模型: {model_path}")
            
            return jsonify({
                'status': 'success',
                'message': f'成功加载模型: {model_path}',
                'mode': 'mock' if use_mock else 'normal'
            })
        except Exception as e:
            logger.error(f"加载模型失败: {str(e)}")
            return jsonify({'error': f'加载模型失败: {str(e)}'}), 500
        
    except Exception as e:
        logger.error(f"加载模型请求处理失败: {str(e)}")
        return jsonify({'error': str(e)}), 500 