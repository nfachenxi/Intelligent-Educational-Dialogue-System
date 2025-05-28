# 智能教育对话系统项目结构

## 目录结构

```
intelligent_edu_system/
├── app/                        # 应用程序包
│   ├── extensions.py           # Flask扩展定义
│   ├── __init__.py             # 应用初始化
│   ├── models/                 # 数据库模型
│   │   ├── __init__.py         # 模型包初始化
│   │   ├── chat.py             # 聊天相关模型
│   │   ├── chat_history.py     # 对话历史模型
│   │   ├── chat_session.py     # 会话模型
│   │   ├── gpt2.py             # GPT-2模型
│   │   ├── knowledge_base.py   # 知识库模型
│   │   └── user.py             # 用户模型
│   ├── routes/                 # 路由处理
│   │   ├── __init__.py         # 路由包初始化
│   │   ├── aiml.py             # AIML规则路由
│   │   ├── auth.py             # 认证路由
│   │   ├── chat.py             # 聊天路由
│   │   ├── gpt2.py             # GPT-2路由
│   │   └── main.py             # 主页路由
│   ├── services/               # 服务层
│   │   ├── __init__.py         # 服务包初始化
│   │   ├── aiml_manager.py     # AIML管理服务
│   │   └── aiml_service.py     # AIML对话服务
│   ├── static/                 # 静态资源
│   │   ├── css/                # CSS样式文件
│   │   ├── js/                 # JavaScript脚本
│   │   └── img/                # 图片资源
│   ├── templates/              # HTML模板
│   │   ├── base.html           # 基础模板
│   │   ├── index.html          # 主页模板
│   │   ├── aiml_chat.html      # AIML对话页面
│   │   └── gpt2_chat.html      # GPT-2对话页面
│   └── utils/                  # 工具函数
│       ├── __init__.py         # 工具包初始化
│       └── validators.py       # 验证工具
├── data/                       # 数据文件
│   ├── aiml/                   # AIML规则文件
│   │   ├── bootstrap.xml       # 初始化文件
│   │   ├── education.aiml      # 教育规则
│   │   ├── greeting.aiml       # 问候规则
│   │   ├── subjects.aiml       # 学科规则
│   │   └── custom.aiml         # 自定义规则
│   ├── models/                 # 预训练模型
│   │   └── gpt2/               # GPT-2模型文件
│   ├── training_data/          # 模型训练数据
│   └── knowledge_graph/        # 知识图谱数据
├── tests/                      # 测试用例
│   ├── __init__.py             # 测试包初始化
│   ├── conftest.py             # 测试配置
│   ├── create_test_user.py     # 测试用户创建
│   ├── test_aiml.py            # AIML测试
│   ├── test_api.py             # API测试
│   ├── test_api_request.py     # API请求测试
│   ├── test_chat.py            # 聊天测试
│   └── test_gpt2.py            # GPT-2测试
├── test_logs/                  # 测试日志
│   ├── coverage_report.txt     # 覆盖率报告
│   ├── test_output.txt         # 测试输出
│   └── test_report.md          # 测试报告
├── docs/                       # 文档文件
│   ├── index.md                # 文档索引
│   ├── api_testing.md          # API测试文档
│   ├── installation_guide.md   # 安装指南
│   ├── roadmap.md              # 发展规划
│   ├── requirements_spec.md    # 项目需求规格
│   └── phase1_summary.md       # 第一阶段总结
├── config.py                   # 配置文件
├── README.md                   # 项目说明
├── requirements.txt            # 依赖列表
├── run.py                      # 应用入口
├── test_aiml_api.py            # AIML API测试脚本
└── test_gpt2_api.py            # GPT-2 API测试脚本
```

## 模块说明

### 核心模块

1. **AIML规则对话模块**
   - 基于AIML的模板匹配对话系统
   - 支持添加、修改、删除规则
   - 提供学习功能，可动态添加规则

2. **GPT-2生成式对话模块**
   - 基于预训练语言模型的生成式对话
   - 支持上下文多轮对话
   - 提供文本生成功能
   - 支持模型微调

3. **用户认证模块**
   - 用户注册、登录、注销
   - 权限管理和访问控制
   - Token认证机制

4. **会话管理模块**
   - 创建、查询、更新、归档会话
   - 消息存储和检索
   - 上下文维护

### 数据流向

1. **用户请求流程**
   ```
   客户端 -> 认证中间件 -> 路由分发 -> 服务处理 -> 数据库操作 -> 响应返回
   ```

2. **对话处理流程**
   ```
   用户输入 -> AIML匹配/GPT-2生成 -> 响应生成 -> 存储对话历史 -> 返回响应
   ```

## 技术栈

- **Web框架**: Flask 3.0.2
- **数据库**: SQLAlchemy 2.0.28 + SQLite
- **AI模型**: 
  - PyTorch 2.2.1
  - Transformers 4.38.2
- **NLP工具**:
  - NLTK 3.8.1
  - spaCy 3.7.2
- **对话引擎**:
  - python-aiml 0.9.3
- **知识图谱**: RDFLib 7.0.0
- **测试工具**: pytest 8.1.1
- **前端框架**:
  - Bootstrap 5.3.0
  - jQuery 3.6.0

## API接口

### 1. 认证API
- POST /auth/register: 用户注册
- POST /auth/login: 用户登录
- POST /auth/refresh: 刷新令牌
- GET /auth/user: 获取用户信息

### 2. 会话API
- GET /chat/sessions: 获取会话列表
- POST /chat/sessions: 创建新会话
- GET /chat/sessions/<id>: 获取会话详情
- PUT /chat/sessions/<id>: 更新会话
- DELETE /chat/sessions/<id>: 删除会话
- POST /chat/sessions/<id>/messages: 发送消息
- POST /chat/sessions/<id>/archive: 归档会话

### 3. AIML API
- POST /aiml/chat: 发送消息获取响应
  - 参数: message, session_id(可选)
  - 返回: response, session_id
- GET /aiml/files: 获取规则文件列表
- GET /aiml/files/<filename>: 获取规则文件内容
- POST /aiml/files: 创建规则文件
- PUT /aiml/files/<filename>: 更新规则文件
- DELETE /aiml/files/<filename>: 删除规则文件
- GET /aiml/patterns/<filename>: 获取规则列表
- POST /aiml/patterns: 添加规则
- POST /aiml/import: 批量导入规则
- POST /aiml/learn: 学习新规则

### 4. GPT-2 API
- POST /gpt2/chat: 发送消息获取响应
  - 参数: message, session_id(可选)
  - 返回: response, session_id
- GET /gpt2/status: 获取模型状态
  - 返回: status, mode, model_name
- POST /gpt2/generate: 生成文本
  - 参数: prompt, max_length, num_sequences, temperature, top_k, top_p
  - 返回: generated_texts
- POST /gpt2/finetune: 微调模型
  - 参数: train_data_path, num_epochs
  - 返回: status, message, output_dir
- POST /gpt2/upload_data: 上传训练数据
  - 参数: file
  - 返回: status, message, file_path
- GET /gpt2/models: 获取可用模型列表
- POST /gpt2/load_model: 加载指定模型

## 数据模型

### 1. User(用户模型)
- id: 主键
- username: 用户名
- email: 邮箱
- password_hash: 密码哈希
- role: 角色(学生/教师/管理员)
- created_at: 创建时间
- last_login: 最后登录时间

### 2. ChatSession(会话模型)
- id: 主键
- user_id: 用户ID
- name: 会话名称
- created_at: 创建时间
- updated_at: 更新时间
- is_archived: 是否归档

### 3. Message(消息模型)
- id: 主键
- session_id: 会话ID
- role: 角色(user/assistant)
- content: 消息内容
- created_at: 创建时间

### 4. KnowledgeBase(知识库)
- id: 主键
- question: 问题
- answer: 答案
- category: 类别
- subject: 学科
- difficulty: 难度
- usage_count: 使用次数
- accuracy: 正确率
- created_at: 创建时间
- updated_at: 更新时间

## 前端页面

### 1. 主页(index.html)
- 项目介绍
- 功能导航
- 使用说明

### 2. AIML对话页面(aiml_chat.html)
- 实时对话界面
- 对话历史显示
- 会话管理功能
- 知识库显示

### 3. GPT-2对话页面(gpt2_chat.html)
- 上下文对话界面
- 高级生成设置
- 会话管理功能
- 模型状态显示

### 4. 基础模板(base.html)
- 导航栏
- 页面布局
- 公共样式
- 响应式设计 