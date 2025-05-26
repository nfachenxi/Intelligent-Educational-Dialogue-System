# -*- coding: utf-8 -*-
import requests
import json
import os

BASE_URL = 'http://127.0.0.1:5000'

def test_login(username='test_user', password='test123'):
    """测试登录并返回访问令牌"""
    url = f'{BASE_URL}/auth/login'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=data)
    print('登录状态码:', response.status_code)
    
    try:
        result = response.json()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 保存token到文件中以便后续使用
        if 'access_token' in result:
            token_file = os.path.join(os.path.dirname(__file__), 'token.txt')
            with open(token_file, 'w') as f:
                f.write(result['access_token'])
            print(f'Token已保存到: {token_file}')
            
        return result.get('access_token')
    except Exception as e:
        print('解析响应出错:', e)
        return None

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

def test_register(username='test_user', email='test@example.com', password='test123'):
    """测试用户注册"""
    url = f'{BASE_URL}/auth/register'
    data = {
        'username': username,
        'email': email,
        'password': password,
        'role': 'student'
    }
    response = requests.post(url, json=data)
    print('注册状态码:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    
    return response.json()

def test_user_info(access_token):
    """测试获取用户信息"""
    url = f'{BASE_URL}/auth/user'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    print('用户信息状态码:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    
    return response.json()

def test_refresh_token(refresh_token):
    """测试刷新token"""
    url = f'{BASE_URL}/auth/refresh'
    headers = {'Authorization': f'Bearer {refresh_token}'}
    response = requests.post(url, headers=headers)
    print('刷新Token状态码:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    
    return response.json()

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