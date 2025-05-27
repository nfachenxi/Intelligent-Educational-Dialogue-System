"""
GPT-2模块功能测试
"""
import os
import sys
import json
import pytest
from flask import Flask

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 创建测试应用上下文
app = Flask(__name__)
app.config['TESTING'] = True

# 导入自定义的GPT2Generator类
from app.models.gpt2 import GPT2Generator

@pytest.fixture
def app_context():
    """提供应用上下文"""
    with app.app_context():
        yield

def test_gpt2_init(app_context):
    """测试GPT-2初始化"""
    # 使用模拟模式初始化
    generator = GPT2Generator(use_mock=True)
    assert generator is not None
    assert generator.use_mock is True
    assert generator.tokenizer is None
    assert generator.model is None

def test_gpt2_generate_mock(app_context):
    """测试GPT-2生成功能（模拟模式）"""
    generator = GPT2Generator(use_mock=True)
    
    # 测试生成单个文本
    prompt = "人工智能是什么？"
    result = generator.generate(prompt)
    assert isinstance(result, list)
    assert len(result) == 1
    assert prompt in result[0]
    
    # 测试生成多个文本
    result = generator.generate(prompt, num_return_sequences=3)
    assert isinstance(result, list)
    assert len(result) == 3
    for text in result:
        assert prompt in text

def test_gpt2_chat_mock(app_context):
    """测试GPT-2对话功能（模拟模式）"""
    generator = GPT2Generator(use_mock=True)
    
    # 测试无上下文对话
    message = "什么是人工智能？"
    response = generator.chat(message)
    assert isinstance(response, str)
    assert "模拟回复" in response
    
    # 测试有上下文对话
    context = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好，有什么可以帮助你的？"}
    ]
    response = generator.chat(message, context)
    assert isinstance(response, str)
    assert "模拟回复" in response
    assert "上下文中有" in response

def test_format_context(app_context):
    """测试上下文格式化"""
    generator = GPT2Generator(use_mock=True)
    
    context = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好，有什么可以帮助你的？"},
        {"role": "user", "content": "我想了解人工智能"}
    ]
    
    formatted = generator._format_context(context)
    assert "用户: 你好" in formatted
    assert "助手: 你好，有什么可以帮助你的？" in formatted
    assert "用户: 我想了解人工智能" in formatted

def test_empty_context(app_context):
    """测试空上下文"""
    generator = GPT2Generator(use_mock=True)
    
    formatted = generator._format_context([])
    assert formatted == ""
    
    formatted = generator._format_context(None)
    assert formatted == ""

if __name__ == "__main__":
    # 运行测试
    pytest.main(["-v", __file__]) 