# -*- coding: utf-8 -*-
import requests

def test_server():
    try:
        response = requests.get('http://127.0.0.1:5000/')
        print('服务器状态码:', response.status_code)
        print('服务器响应:', response.text)
    except Exception as e:
        print('连接错误:', e)

if __name__ == '__main__':
    test_server() 