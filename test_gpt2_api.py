import requests
import json

def test_gpt2_chat():
    """测试GPT-2聊天API接口"""
    url = "http://127.0.0.1:5000/gpt2/chat"
    headers = {"Content-Type": "application/json"}
    data = {"message": "什么是机器学习?"}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"GPT-2回复: {result.get('response', '没有返回response字段')}")
        else:
            print(f"错误: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

if __name__ == "__main__":
    test_gpt2_chat() 