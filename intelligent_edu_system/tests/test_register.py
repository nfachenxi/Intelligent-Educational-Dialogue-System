# -*- coding: utf-8 -*-
import requests

def test_register():
    url = 'http://127.0.0.1:5000/auth/register'
    data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test123',
        'role': 'student'
    }
    response = requests.post(url, json=data)
    print('Status Code:', response.status_code)
    print('Response:', response.text)

if __name__ == '__main__':
    test_register() 