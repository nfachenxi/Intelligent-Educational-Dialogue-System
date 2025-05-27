import pytest
import requests
import sys
import os

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 定义基础URL
BASE_URL = 'http://127.0.0.1:5000'

def test_gpt2_chat(access_token):
    """测试GPT-2对话"""
    url = f'{BASE_URL}/gpt2/chat'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'message': '你好，请介绍一下自己。'}
    response = requests.post(url, json=data, headers=headers)
    print(f"测试GPT-2对话响应: {response.status_code}")
    if response.status_code != 200:
        print(response.text)
    assert response.status_code == 200
    assert 'response' in response.json()

def test_gpt2_chat_with_context(access_token, session_id):
    """测试带上下文的GPT-2对话"""
    url = f'{BASE_URL}/gpt2/chat'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'message': '你好，请介绍一下自己。',
        'session_id': session_id
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"测试带上下文的GPT-2对话响应: {response.status_code}")
    if response.status_code != 200:
        print(response.text)
    assert response.status_code == 200
    assert 'response' in response.json()
    assert 'session_id' in response.json()
    assert response.json()['session_id'] == session_id

def test_gpt2_generate(access_token):
    """测试GPT-2文本生成"""
    url = f'{BASE_URL}/gpt2/generate'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'prompt': '人工智能的未来发展趋势',
        'max_length': 150,
        'num_sequences': 2,
        'temperature': 0.8
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"测试GPT-2文本生成响应: {response.status_code}")
    if response.status_code != 200:
        print(response.text)
    assert response.status_code == 200
    assert 'generated_texts' in response.json()
    assert len(response.json()['generated_texts']) == 2

def test_gpt2_chat_empty_message(access_token):
    """测试空消息"""
    url = f'{BASE_URL}/gpt2/chat'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'message': ''}
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 400
    assert 'error' in response.json()

def test_gpt2_generate_empty_prompt(access_token):
    """测试空提示文本"""
    url = f'{BASE_URL}/gpt2/generate'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'prompt': ''}
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 400
    assert 'error' in response.json()

def test_gpt2_chat_unauthorized():
    """测试未授权访问"""
    url = f'{BASE_URL}/gpt2/chat'
    data = {'message': '你好'}
    response = requests.post(url, json=data)
    assert response.status_code == 401

def test_gpt2_generate_unauthorized():
    """测试未授权访问"""
    url = f'{BASE_URL}/gpt2/generate'
    data = {'prompt': '测试生成'}
    response = requests.post(url, json=data)
    assert response.status_code == 401

# 用于获取token的辅助函数
def get_access_token():
    """获取测试用的访问令牌"""
    url = f'{BASE_URL}/auth/login'
    data = {
        'username': 'test_user',
        'password': 'test123'
    }
    response = requests.post(url, json=data)
    return response.json().get('access_token')

# 用于获取会话ID的辅助函数
def get_session_id(access_token):
    """获取测试用的会话ID"""
    url = f'{BASE_URL}/chat/sessions'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'name': 'Test Session'}
    response = requests.post(url, json=data, headers=headers)
    return response.json().get('session_id')

# 定义pytest fixture
@pytest.fixture
def access_token():
    """获取访问令牌的fixture"""
    return get_access_token()

@pytest.fixture
def session_id(access_token):
    """获取会话ID的fixture"""
    return get_session_id(access_token)

if __name__ == '__main__':
    pytest.main(['-v', 'test_gpt2.py']) 