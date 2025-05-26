# -*- coding: utf-8 -*-
import requests
import json
from test_api import test_login

BASE_URL = 'http://127.0.0.1:5000'

def test_create_session(access_token):
    """测试创建会话"""
    url = f'{BASE_URL}/chat/sessions'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'title': '测试会话',
        'max_context_length': 5,
        'language': 'zh-CN'
    }
    response = requests.post(url, headers=headers, json=data)
    print('创建会话响应:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    return response.json()['session']['session_id']

def test_get_sessions(access_token):
    """测试获取会话列表"""
    url = f'{BASE_URL}/chat/sessions'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    print('获取会话列表响应:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

def test_send_message(access_token, session_id):
    """测试发送消息"""
    url = f'{BASE_URL}/chat/sessions/{session_id}/messages'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'message': '你好，这是一条测试消息',
        'message_type': 'text'
    }
    response = requests.post(url, headers=headers, json=data)
    print('发送消息响应:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

def test_get_session(access_token, session_id):
    """测试获取会话详情"""
    url = f'{BASE_URL}/chat/sessions/{session_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    print('获取会话详情响应:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

def test_update_session(access_token, session_id):
    """测试更新会话"""
    url = f'{BASE_URL}/chat/sessions/{session_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'title': '更新后的会话标题',
        'max_context_length': 10
    }
    response = requests.put(url, headers=headers, json=data)
    print('更新会话响应:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

def test_archive_session(access_token, session_id):
    """测试归档会话"""
    url = f'{BASE_URL}/chat/sessions/{session_id}/archive'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.post(url, headers=headers)
    print('归档会话响应:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    # 先登录获取token
    print('=== 登录获取Token ===')
    access_token = test_login()
    
    print('\n=== 测试创建会话 ===')
    session_id = test_create_session(access_token)
    
    print('\n=== 测试获取会话列表 ===')
    test_get_sessions(access_token)
    
    print('\n=== 测试发送消息 ===')
    test_send_message(access_token, session_id)
    
    print('\n=== 测试获取会话详情 ===')
    test_get_session(access_token, session_id)
    
    print('\n=== 测试更新会话 ===')
    test_update_session(access_token, session_id)
    
    print('\n=== 测试归档会话 ===')
    test_archive_session(access_token, session_id) 