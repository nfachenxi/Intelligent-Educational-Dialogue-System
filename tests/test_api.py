# -*- coding: utf-8 -*-
import requests
import json
import os
import pytest
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
    json_data = response.json()
    assert 'access_token' in json_data
    assert 'refresh_token' in json_data

def test_register():
    """测试用户注册"""
    url = f'{BASE_URL}/auth/register'
    data = {
        'username': 'test_user',
        'password': 'test123',
        'email': 'test@example.com'
    }
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert response.json()['error'] == '用户名已存在'

def test_user_info(access_token):
    """测试获取用户信息"""
    url = f'{BASE_URL}/auth/user'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    user_info = response.json()
    assert 'username' in user_info
    assert 'email' in user_info
    assert 'role' in user_info
    assert user_info['username'] == 'test_user'

def test_refresh_token(refresh_token):
    """测试刷新访问令牌"""
    url = f'{BASE_URL}/auth/refresh'
    headers = {'Authorization': f'Bearer {refresh_token}'}
    response = requests.post(url, headers=headers)
    assert response.status_code == 200
    assert 'access_token' in response.json()

def get_token():
    """获取访问令牌，如果本地文件存在则使用文件中的token，否则重新登录获取"""
    token_file = os.path.join(os.path.dirname(__file__), 'token.txt')
    
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            token = f.read().strip()
            if token:
                # 验证token是否有效
                url = f'{BASE_URL}/auth/user'
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    print('使用缓存的token')
                    return token
    
    # 如果token不存在或已失效，重新登录获取
    return test_login()

if __name__ == '__main__':
    # 测试注册
    print('=== 测试注册用户 ===')
    try:
        test_register()
    except Exception as e:
        print('注册用户出错，可能用户已存在:', e)
    
    # 测试登录
    print('\n=== 测试用户登录 ===')
    token_data = test_login()
    
    if token_data:
        # 测试获取用户信息
        print('\n=== 测试获取用户信息 ===')
        test_user_info(token_data) 