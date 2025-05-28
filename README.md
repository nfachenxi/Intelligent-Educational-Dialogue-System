# 智能教育对话系统

## 项目概述
本项目是一个基于多种技术栈的智能对话系统，专注于教育领域的自然语言交互。系统集成了规则检索、生成式对话、情感分析和知识图谱等多个模块，旨在提供流畅、智能的教育场景对话体验。

## 技术架构

### 核心模块
1. **规则检索对话模块**
   - 基于AIML（人工智能标记语言）
   - 处理基础问答和固定模式对话
   - 实现快速响应的一问一答

2. **生成式对话模块**
   - 基于GPT-2模型微调
   - 支持更灵活的对话生成
   - 针对教育场景的特定训练

3. **情感分析模块**
   - 实时分析用户输入的情感倾向
   - 调整回复的语气和内容
   - 提供个性化的情感响应

4. **知识图谱模块**
   - 使用SPARQL进行知识查询
   - 构建教育领域知识库
   - 增强回答的准确性和专业性

### 系统架构
- 前端：Web界面 (Bootstrap/jQuery)
- 后端：Flask 3.0.2
- 数据库：SQLite + SQLAlchemy 2.0.28
- API接口：RESTful设计

## 当前实现状态

### 已实现功能
1. **基础架构**
   - 完整的Flask应用架构
   - 数据库模型与关系
   - RESTful API接口
   - 前端页面模板

2. **用户认证**
   - 用户注册、登录功能
   - JWT令牌认证
   - 用户权限控制

3. **AIML规则对话**
   - 完整的AIML规则管理
   - 对话会话维护
   - 自定义规则学习
   - 前端实时对话界面

4. **GPT-2生成对话**
   - 基于GPT-2的文本生成
   - 模拟模式支持
   - 上下文对话管理
   - 模型训练和微调接口
   - 前端高级设置界面

5. **会话管理**
   - 会话创建、查询、更新
   - 消息存储与检索
   - 上下文管理

### 待实现功能
1. **情感分析模块**
2. **知识图谱模块**
3. **用户行为分析**
4. **系统评测与优化**

## 安装和运行

### 环境要求
- Python 3.8+
- SQLite 3.0+
- Windows/Linux/MacOS

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/intelligent_edu_system.git
cd intelligent_edu_system
```

2. **创建虚拟环境**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python -m venv venv
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **初始化数据库**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. **运行应用**
```bash
python run.py
```

应用将在 http://127.0.0.1:5000 启动。

### 测试API

项目提供了两个测试脚本：

1. **测试AIML对话**
```bash
python test_aiml_api.py
```

2. **测试GPT-2对话**
```bash
python test_gpt2_api.py
```

## 使用指南

### AIML对话
1. 访问 http://127.0.0.1:5000/aiml/chat.html
2. 在输入框中输入问题，点击发送
3. 系统将基于AIML规则库返回响应
4. 可以清空对话或复制对话记录

### GPT-2对话
1. 访问 http://127.0.0.1:5000/gpt2/chat.html
2. 在输入框中输入问题，点击发送
3. 系统将使用GPT-2模型生成响应
4. 可以通过高级设置调整生成参数

### 管理AIML规则
*需要管理员权限*

1. 登录管理员账户
2. 访问规则管理界面
3. 可以查看、添加、修改、删除规则

### 微调GPT-2模型
*需要管理员权限*

1. 登录管理员账户
2. 上传训练数据
3. 设置训练参数
4. 启动微调过程

## 项目结构

详细的项目结构请参见 [docs/project_structure.md](docs/project_structure.md)

## 开发日志

详细的开发记录请参见 [docs/development_log.md](docs/development_log.md)

## 贡献指南

1. Fork 本仓库
2. 创建新的分支
3. 提交更改
4. 发起 Pull Request

## 许可证

MIT License 