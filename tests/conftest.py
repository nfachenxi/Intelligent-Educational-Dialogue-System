import pytest
import requests

BASE_URL = 'http://127.0.0.1:5000'

@pytest.fixture
def access_token():
    """获取访问令牌的fixture"""
    url = f'{BASE_URL}/auth/login'
    data = {
        'username': 'test_user',
        'password': 'test123'
    }
    response = requests.post(url, json=data)
    return response.json().get('access_token')

@pytest.fixture
def refresh_token():
    """获取刷新令牌的fixture"""
    url = f'{BASE_URL}/auth/login'
    data = {
        'username': 'test_user',
        'password': 'test123'
    }
    response = requests.post(url, json=data)
    return response.json().get('refresh_token')

@pytest.fixture
def session_id(access_token):
    """创建并获取会话ID的fixture"""
    url = f'{BASE_URL}/chat/sessions'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'name': 'Test Session'}
    response = requests.post(url, json=data, headers=headers)
    return response.json().get('session_id')

@pytest.fixture
def filename():
    """返回测试用的AIML文件名"""
    return 'greeting.aiml' 