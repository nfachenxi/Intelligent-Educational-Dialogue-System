# 智能教育对话系统 - 项目结构

> 生成时间: 2025-05-26 21:55:31

## 目录结构

```
intelligent_edu_system/
├── app/                   # 应用主目录
│   ├── __init__.py        # Flask应用工厂
│   ├── models/            # 数据模型
│   │   ├── __init__.py    # 数据库初始化
│   │   ├── user.py        # 用户模型
│   │   ├── chat_history.py # 对话历史模型
│   │   ├── chat_session.py # 会话模型
│   │   └── knowledge_base.py # 知识库模型
│   ├── routes/            # 路由控制器
│   │   ├── __init__.py    # 路由包初始化
│   │   ├── main.py        # 主路由
│   │   ├── auth.py        # 认证路由
│   │   ├── chat.py        # 会话管理路由
│   │   └── aiml.py        # AIML管理路由
│   ├── services/          # 业务逻辑服务
│   │   ├── __init__.py    # 服务包初始化
│   │   ├── aiml_service.py # AIML对话服务
│   │   └── aiml_manager.py # AIML规则管理服务
│   └── utils/             # 工具函数
│       ├── __init__.py    # 工具包初始化
│       └── email_validator.py # 邮箱验证工具
├── config/                # 配置目录
│   └── default.py         # 默认配置
├── data/                  # 数据存储
│   ├── app.db             # SQLite数据库
│   └── aiml/              # AIML规则文件
│       ├── bootstrap.xml  # 引导文件
│       ├── greeting.aiml  # 问候规则
│       ├── education.aiml # 教育规则
│       ├── subjects.aiml  # 学科规则
│       └── custom.aiml    # 自定义规则
├── docs/                  # 项目文档
│   ├── development_plan.md # 开发方案
│   └── api_docs.md        # API文档
├── migrations/            # 数据库迁移文件
├── tests/                 # 测试用例
│   ├── __init__.py        # 测试包初始化
│   ├── test_server.py     # 服务器测试
│   ├── test_api.py        # API测试工具
│   ├── test_register.py   # 注册功能测试
│   ├── test_chat.py       # 会话功能测试
│   └── test_aiml.py       # AIML功能测试
├── venv/                  # 虚拟环境
├── activate.bat           # 环境变量设置脚本
├── app.log                # 应用日志
├── dev_log.md             # 开发日志
├── development_log.md     # 更详细的开发日志
├── manage.py              # 数据库迁移管理
├── project_structure.md   # 项目结构文档
├── requirements.txt       # 项目依赖
├── run.py                 # 应用入口
└── README.md              # 项目说明
```

## 模块说明

### 核心模块

1. **用户管理模块**
   - 用户注册、登录和认证
   - JWT令牌管理
   - 用户信息管理

2. **会话管理模块**
   - 创建和管理对话会话
   - 消息发送和接收
   - 会话状态管理（活动/归档/删除）

3. **AIML规则对话模块**
   - AIML规则解析和匹配
   - 基于规则的对话生成
   - 规则文件管理和编辑
   - 与会话管理的集成

4. **知识库模块**（待实现）
   - 教育领域知识存储
   - 问答对管理
   - 知识检索

### AIML规则文件

1. **bootstrap.xml**
   - 引导文件，用于加载所有AIML规则文件
   - 包含默认回复和系统命令

2. **greeting.aiml**
   - 问候规则，处理基本问候和对话开场
   - 包含机器人自我介绍和帮助信息

3. **education.aiml**
   - 通用教育规则，处理学习方法、技巧等
   - 提供学习计划、记忆方法、考试技巧等建议

4. **subjects.aiml**
   - 学科知识规则，包含数学、物理、化学等学科的基础问答
   - 提供不同学科的学习方法建议

5. **custom.aiml**
   - 自定义规则文件，用于存储用户添加的新规则
   - 通过API动态更新

### 数据模型

1. **User**
   - 用户基本信息
   - 认证和权限

2. **ChatSession**
   - 会话元数据
   - 会话配置和状态

3. **ChatHistory**
   - 对话历史记录
   - 消息和响应内容
   - 对话分析信息
   - 回复来源标记（aiml/gpt/knowledge_base）

4. **KnowledgeBase**
   - 知识条目
   - 分类和统计信息

### API接口

1. **认证API**
   - POST /auth/register：用户注册
   - POST /auth/login：用户登录
   - POST /auth/refresh：刷新令牌
   - GET /auth/user：获取用户信息

2. **会话API**
   - GET /chat/sessions：获取会话列表
   - POST /chat/sessions：创建新会话
   - GET /chat/sessions/<session_id>：获取会话详情
   - PUT /chat/sessions/<session_id>：更新会话
   - DELETE /chat/sessions/<session_id>：删除会话
   - POST /chat/sessions/<session_id>/messages：发送消息（已集成AIML）
   - POST /chat/sessions/<session_id>/archive：归档会话

3. **AIML API**
   - POST /aiml/chat：发送消息获取AIML响应
   - GET /aiml/files：获取AIML文件列表
   - GET /aiml/files/<filename>：获取AIML文件内容
   - POST /aiml/files：创建AIML文件
   - PUT /aiml/files/<filename>：更新AIML文件
   - DELETE /aiml/files/<filename>：删除AIML文件
   - GET /aiml/patterns/<filename>：获取文件中的规则
   - POST /aiml/patterns：添加规则
   - POST /aiml/import：批量导入规则
   - POST /aiml/learn：学习新规则 