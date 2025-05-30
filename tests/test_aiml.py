# -*- coding: utf-8 -*-
import requests
import json
from test_api import test_login
import pytest
from conftest import BASE_URL

def test_aiml_chat(access_token, session_id=None):
    """测试AIML对话功能"""
    url = f'{BASE_URL}/aiml/chat'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'message': '你好',
        'session_id': session_id
    }
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 200
    assert 'response' in response.json()
    print('AIML对话响应:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    
    return response.json()

def test_get_aiml_files(access_token):
    """测试获取AIML文件列表"""
    url = f'{BASE_URL}/aiml/files'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    files = response.json()
    assert isinstance(files, list)
    assert len(files) > 0
    print('获取AIML文件列表响应:', response.status_code)
    print(json.dumps(files, ensure_ascii=False, indent=2))
    
    return files

def test_get_file_content(access_token, filename):
    """测试获取AIML文件内容"""
    url = f'{BASE_URL}/aiml/files/{filename}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    content = response.json()
    assert 'content' in content
    assert isinstance(content['content'], str)
    print('获取AIML文件内容响应:', response.status_code)
    print(json.dumps(content, ensure_ascii=False, indent=2))
    
    return content

def test_create_file(access_token):
    """测试创建AIML文件"""
    url = f'{BASE_URL}/aiml/files'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'filename': 'test.aiml',
        'categories': [
            ('测试问题', '这是测试回答'),
            ('测试 *', '我不知道关于<star/>的信息')
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 201
    print('创建AIML文件响应:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    
    return response.json()

def test_add_pattern(access_token, filename='greeting.aiml'):
    """测试添加AIML模式"""
    url = f'{BASE_URL}/aiml/patterns'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'filename': filename,
        'pattern': '怎么学习编程',
        'template': '学习编程需要掌握基础语法，多做练习，参与实际项目。建议从Python等简单语言开始学习。'
    }
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 201
    print('添加AIML模式响应:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    
    # 测试新添加的模式
    test_data = {
        'message': '怎么学习编程',
        'session_id': None
    }
    chat_response = requests.post(f'{BASE_URL}/aiml/chat', headers=headers, json=test_data)
    assert chat_response.status_code == 200
    print('测试新添加模式响应:')
    print(json.dumps(chat_response.json(), ensure_ascii=False, indent=2))
    
    return response.json()

def test_get_patterns(access_token, filename='greeting.aiml'):
    """测试获取AIML文件中的模式"""
    url = f'{BASE_URL}/aiml/patterns/{filename}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    patterns = response.json()
    assert isinstance(patterns, list)
    print('获取AIML模式响应:', response.status_code)
    print(json.dumps(patterns, ensure_ascii=False, indent=2))
    
    return patterns

def test_learn_pattern(access_token):
    """测试学习新模式"""
    url = f'{BASE_URL}/aiml/learn'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'pattern': '推荐一些学习资源',
        'template': '推荐以下学习资源：1. 在线教程网站如Coursera, edX等；2. 编程社区如GitHub, Stack Overflow；3. 官方文档；4. 技术博客和书籍。'
    }
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 201
    print('学习新模式响应:', response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    
    # 测试新学习的模式
    test_data = {
        'message': '推荐一些学习资源',
        'session_id': None
    }
    chat_response = requests.post(f'{BASE_URL}/aiml/chat', headers=headers, json=test_data)
    assert chat_response.status_code == 200
    print('测试新学习模式响应:')
    print(json.dumps(chat_response.json(), ensure_ascii=False, indent=2))
    
    return response.json()

def test_chat(access_token):
    """测试AIML对话"""
    url = f'{BASE_URL}/aiml/chat'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'input': 'Hello'}
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 200
    assert 'response' in response.json()

def test_get_files(access_token):
    """测试获取AIML文件列表"""
    url = f'{BASE_URL}/aiml/files'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    files = response.json()
    assert isinstance(files, list)
    assert len(files) > 0

def test_get_file_content(access_token, filename):
    """测试获取AIML文件内容"""
    url = f'{BASE_URL}/aiml/files/{filename}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    content = response.json()
    assert 'content' in content
    assert isinstance(content['content'], str)

def test_upload_file(access_token):
    """测试上传AIML文件"""
    url = f'{BASE_URL}/aiml/files'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'filename': 'test.aiml',
        'content': '''<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <category>
        <pattern>TEST UPLOAD</pattern>
        <template>Upload successful!</template>
    </category>
</aiml>'''
    }
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code in [201, 400]  # 400表示文件已存在

def test_get_patterns(access_token):
    """测试获取AIML模式列表"""
    url = f'{BASE_URL}/aiml/patterns/{filename}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    patterns = response.json()
    assert isinstance(patterns, list)

def test_add_pattern(access_token):
    """测试添加AIML模式"""
    url = f'{BASE_URL}/aiml/patterns'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'pattern': 'TEST PATTERN',
        'template': 'This is a test response',
        'filename': 'test.aiml'
    }
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 201

def test_learn_aiml(access_token):
    """测试学习AIML文件"""
    url = f'{BASE_URL}/aiml/learn'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'filename': 'test.aiml'}
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 201

def test_chat_after_learn(access_token):
    """测试学习后的对话"""
    url = f'{BASE_URL}/aiml/chat'
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'input': 'TEST PATTERN'}
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()['response'] == 'This is a test response'

def run_complete_test():
    """运行完整测试流程"""
    # 1. 登录获取token
    print('=== 登录获取Token ===')
    access_token = test_login()
    
    # 2. 测试对话功能
    print('\n=== 测试AIML对话功能 ===')
    test_aiml_chat(access_token)
    
    # 3. 测试获取文件列表
    print('\n=== 测试获取AIML文件列表 ===')
    files_result = test_get_aiml_files(access_token)
    
    # 4. 如果有文件，测试获取文件内容
    if files_result and len(files_result) > 0:
        filename = files_result[0]
        print(f'\n=== 测试获取AIML文件内容 ({filename}) ===')
        test_get_file_content(access_token, filename)
    
    # 5. 测试创建文件
    print('\n=== 测试创建AIML文件 ===')
    test_create_file(access_token)
    
    # 6. 测试添加模式
    print('\n=== 测试添加AIML模式 ===')
    test_add_pattern(access_token)
    
    # 7. 测试获取模式
    print('\n=== 测试获取AIML模式 ===')
    test_get_patterns(access_token)
    
    # 8. 测试学习新模式
    print('\n=== 测试学习新模式 ===')
    test_learn_pattern(access_token)

if __name__ == '__main__':
    run_complete_test() 