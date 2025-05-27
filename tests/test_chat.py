# -*- coding: utf-8 -*-
import pytest
import requests
from conftest import BASE_URL

def test_login():
    """测试用户登录"""
    url = f'{BASE_URL}/auth/login'
    data = {
        'username': 'test_user',
        'password': 'test123'
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert 'access_token' in response.json()

def test_create_session(access_token):
    """测试创建会话"""
    url = f'{BASE_URL}/chat/sessions'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'name': 'Test Session'}
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 201
    assert 'session_id' in response.json()

def test_get_sessions(access_token):
    """测试获取会话列表"""
    url = f'{BASE_URL}/chat/sessions'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    sessions = response.json()
    assert isinstance(sessions, list)
    assert len(sessions) > 0

def test_send_message(access_token, session_id):
    """测试发送消息"""
    url = f'{BASE_URL}/chat/sessions/{session_id}/messages'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'content': 'Hello, AI!'}
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 201
    assert 'message_id' in response.json()

def test_get_session(access_token, session_id):
    """测试获取单个会话"""
    url = f'{BASE_URL}/chat/sessions/{session_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    session = response.json()
    assert 'id' in session
    assert 'name' in session
    assert 'messages' in session

def test_update_session(access_token, session_id):
    """测试更新会话"""
    url = f'{BASE_URL}/chat/sessions/{session_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'name': 'Updated Session Name'}
    response = requests.put(url, json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()['name'] == 'Updated Session Name'

def test_archive_session(access_token, session_id):
    """测试归档会话"""
    url = f'{BASE_URL}/chat/sessions/{session_id}/archive'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.post(url, headers=headers)
    assert response.status_code == 200
    assert response.json()['archived'] == True

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