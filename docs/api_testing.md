# 智能教育对话系统API测试指南

本文档提供了智能教育对话系统各个API端点的测试方法和示例。

## 测试环境准备

1. 确保系统已启动
   ```bash
   python run.py
   ```

2. 准备API测试工具
   - 可以使用Postman、curl或其他HTTP客户端
   - 也可以使用提供的测试脚本

## AIML对话API测试

### 测试方法1：使用测试脚本

系统提供了一个简单的测试脚本`test_aiml_api.py`，可以直接运行：

```bash
python test_aiml_api.py
```

输出示例：
```
状态码: 200
响应内容: {"response":"你好！我是智能教育助手，有什么可以帮助你的吗？","session_id":null}
AIML回复: 你好！我是智能教育助手，有什么可以帮助你的吗？
```

### 测试方法2：HTTP请求

可以使用curl或其他HTTP客户端测试：

```bash
curl -X POST http://127.0.0.1:5000/aiml/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"你好"}'
```

响应示例：
```json
{
  "response": "你好！我是智能教育助手，有什么可以帮助你的吗？",
  "session_id": null
}
```

### 高级测试：会话管理

```bash
# 第一次请求，获取会话ID
curl -X POST http://127.0.0.1:5000/aiml/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"你好"}'

# 使用获取的会话ID进行第二次请求
curl -X POST http://127.0.0.1:5000/aiml/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"如何学习数学", "session_id":"SESSION_ID_HERE"}'
```

## GPT-2对话API测试

### 测试方法1：使用测试脚本

系统提供了一个简单的测试脚本`test_gpt2_api.py`，可以直接运行：

```bash
python test_gpt2_api.py
```

输出示例：
```
状态码: 200
GPT-2回复: 机器学习是人工智能的一个分支，它使用算法和统计模型，使计算机系统能够从数据中学习和改进，而无需明确编程。通过分析大量数据，机器学习系统可以识别模式并做出决策，随着新数据的增加而不断改进其性能。
```

### 测试方法2：HTTP请求

可以使用curl或其他HTTP客户端测试：

```bash
curl -X POST http://127.0.0.1:5000/gpt2/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"什么是机器学习?"}'
```

响应示例：
```json
{
  "response": "机器学习是人工智能的一个分支，它使用算法和统计模型，使计算机系统能够从数据中学习和改进，而无需明确编程。通过分析大量数据，机器学习系统可以识别模式并做出决策，随着新数据的增加而不断改进其性能。",
  "session_id": null
}
```

### 测试GPT-2状态

```bash
curl -X GET http://127.0.0.1:5000/gpt2/status
```

响应示例：
```json
{
  "status": "ok",
  "mode": "mock",
  "model_name": "gpt2"
}
```

### 测试文本生成

需要JWT认证，先获取令牌：

```bash
# 登录获取JWT令牌
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin", "password":"password"}'

# 使用令牌生成文本
curl -X POST http://127.0.0.1:5000/gpt2/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "prompt": "人工智能正在改变教育方式，",
    "max_length": 100,
    "num_sequences": 1,
    "temperature": 0.7
  }'
```

## 用户认证API测试

### 用户注册

```bash
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "password123"
  }'
```

### 用户登录

```bash
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "password123"
  }'
```

响应将包含JWT令牌，用于后续的认证请求。

### 刷新令牌

```bash
curl -X POST http://127.0.0.1:5000/auth/refresh \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 会话管理API测试

### 获取会话列表

```bash
curl -X GET http://127.0.0.1:5000/chat/sessions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 创建新会话

```bash
curl -X POST http://127.0.0.1:5000/chat/sessions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "我的学习会话"
  }'
```

### 获取会话详情

```bash
curl -X GET http://127.0.0.1:5000/chat/sessions/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 发送消息

```bash
curl -X POST http://127.0.0.1:5000/chat/sessions/1/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "content": "什么是机器学习?"
  }'
```

## 常见问题排查

### 连接问题
- 确认服务器正在运行
- 检查端口是否正确（默认5000）
- 确认没有防火墙阻止

### 认证问题
- JWT令牌格式必须正确
- 令牌可能已过期，需要刷新
- 确认用户权限足够

### 数据问题
- 请求格式必须是正确的JSON
- 请求体中必须包含所有必需字段
- 字段类型必须正确

## 性能测试

可以使用ApacheBench或JMeter进行性能测试：

```bash
ab -n 100 -c 10 -p payload.json -T application/json http://127.0.0.1:5000/aiml/chat
```

其中payload.json内容为：
```json
{"message":"你好"}
```

## 后续扩展

随着情感分析和知识图谱模块的开发，将会添加更多API端点的测试方法。请关注文档更新。 