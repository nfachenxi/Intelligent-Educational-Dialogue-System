"""
测试API请求
"""
import requests
import json

# 登录获取token
def get_token():
    url = "http://127.0.0.1:5000/auth/login"
    headers = {"Content-Type": "application/json"}
    data = {"username": "test_user", "password": "test123"}
    response = requests.post(url, headers=headers, json=data)
    
    print(f"登录状态码: {response.status_code}")
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"Token: {token[:20]}...")
        return token
    else:
        print(response.text)
        return None

# 测试GPT-2聊天API
def test_gpt2_chat(token):
    url = "http://127.0.0.1:5000/gpt2/chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {"message": "Hello GPT-2!"}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"GPT-2聊天状态码: {response.status_code}")
        print(response.text)
    except Exception as e:
        print(f"请求异常: {str(e)}")

if __name__ == "__main__":
    token = get_token()
    if token:
        test_gpt2_chat(token) 