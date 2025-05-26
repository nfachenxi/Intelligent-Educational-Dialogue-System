# -*- coding: utf-8 -*-
import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def test_register():
    """测试用户注册"""
    url = f'{BASE_URL}/auth/register'
    data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test123',
        'role': 'student'
    }
    response = requests.post(url, json=data)
    print('注册响应:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

def test_login():
    """测试用户登录"""
    url = f'{BASE_URL}/auth/login'
    data = {
        'username': 'test_user',
        'password': 'test123'
    }
    response = requests.post(url, json=data)
    print('登录响应:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    return response.json().get('access_token')

def test_profile(access_token):
    """测试获取用户信息"""
    url = f'{BASE_URL}/auth/profile'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    print('获取用户信息响应:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    print('=== 测试用户注册 ===')
    test_register()
    print('\n=== 测试用户登录 ===')
    access_token = test_login()
    print('\n=== 测试获取用户信息 ===')
    test_profile(access_token) 