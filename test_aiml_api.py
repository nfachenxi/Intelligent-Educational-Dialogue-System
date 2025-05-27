import requests
import json

def test_aiml_chat():
    """测试AIML聊天API接口"""
    url = "http://127.0.0.1:5000/aiml/chat"
    headers = {"Content-Type": "application/json"}
    data = {"message": "你好"}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"AIML回复: {result['response']}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

if __name__ == "__main__":
    test_aiml_chat() 