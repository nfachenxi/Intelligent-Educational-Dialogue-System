"""
GPT-2模块独立测试（不依赖Flask应用上下文）
"""
import os
import sys
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入GPT-2生成器
from app.models.gpt2 import GPT2Generator

def test_init():
    """测试初始化"""
    generator = GPT2Generator(use_mock=True)
    print(f"模型初始化成功，使用模拟模式：{generator.use_mock}")
    
def test_generate():
    """测试文本生成"""
    generator = GPT2Generator(use_mock=True)
    
    prompt = "人工智能是什么？"
    result = generator.generate(prompt)
    
    print(f"提示: {prompt}")
    print(f"生成结果: {result}")
    
def test_chat():
    """测试对话"""
    generator = GPT2Generator(use_mock=True)
    
    message = "请介绍一下牛顿的三大定律"
    context = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好，有什么可以帮助你的？"}
    ]
    
    response = generator.chat(message, context)
    
    print(f"用户: {message}")
    print(f"助手: {response}")
    
def test_format_context():
    """测试上下文格式化"""
    generator = GPT2Generator(use_mock=True)
    
    context = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好，有什么可以帮助你的？"},
        {"role": "user", "content": "我想了解人工智能"}
    ]
    
    formatted = generator._format_context(context)
    print(f"格式化上下文:\n{formatted}")

if __name__ == "__main__":
    print("===== 测试GPT-2模块 =====")
    
    try:
        print("\n1. 测试初始化")
        test_init()
        
        print("\n2. 测试文本生成")
        test_generate()
        
        print("\n3. 测试对话")
        test_chat()
        
        print("\n4. 测试上下文格式化")
        test_format_context()
        
        print("\n所有测试完成!")
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc() 