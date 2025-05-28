# 智能教育对话系统文档索引

欢迎使用智能教育对话系统文档！本索引将帮助您快速找到所需的信息。

## 项目概述文档

- [README.md](../README.md) - 项目简介、架构概览和基本使用说明
- [project_structure.md](project_structure.md) - 详细的项目结构、模块说明和API接口文档

## 开发文档

- [development_log.md](development_log.md) - 项目开发日志，记录了项目的开发历程和重要里程碑
- [roadmap.md](roadmap.md) - 项目发展规划，包括已完成功能、进行中的工作和未来计划
- [phase1_summary.md](phase1_summary.md) - 第一阶段开发总结，包括已完成工作和技术难点解决

## 需求与规格

- [requirements_spec.md](requirements_spec.md) - 项目需求规格说明，包括功能需求和技术需求

## 安装与配置

- [installation_guide.md](installation_guide.md) - 详细的安装步骤、环境配置和排障指南
- [../requirements.txt](../requirements.txt) - 项目依赖列表

## API与测试

- [api_testing.md](api_testing.md) - API测试指南，包括各个端点的测试方法和示例
- [../test_aiml_api.py](../test_aiml_api.py) - AIML对话API测试脚本
- [../test_gpt2_api.py](../test_gpt2_api.py) - GPT-2对话API测试脚本

## 模块文档

### 核心模块

- **AIML规则对话模块**
  - [../app/services/aiml_service.py](../app/services/aiml_service.py) - AIML服务实现
  - [../app/services/aiml_manager.py](../app/services/aiml_manager.py) - AIML规则管理
  - [../app/routes/aiml.py](../app/routes/aiml.py) - AIML路由定义

- **GPT-2生成对话模块**
  - [../app/models/gpt2.py](../app/models/gpt2.py) - GPT-2模型实现
  - [../app/routes/gpt2.py](../app/routes/gpt2.py) - GPT-2路由定义

- **用户认证模块**
  - [../app/routes/auth.py](../app/routes/auth.py) - 认证路由
  - [../app/models/user.py](../app/models/user.py) - 用户模型

- **会话管理模块**
  - [../app/routes/chat.py](../app/routes/chat.py) - 会话路由
  - [../app/models/chat_session.py](../app/models/chat_session.py) - 会话模型
  - [../app/models/chat.py](../app/models/chat.py) - 聊天模型

### 前端模板

- [../app/templates/base.html](../app/templates/base.html) - 基础模板
- [../app/templates/index.html](../app/templates/index.html) - 主页模板
- [../app/templates/aiml_chat.html](../app/templates/aiml_chat.html) - AIML对话页面
- [../app/templates/gpt2_chat.html](../app/templates/gpt2_chat.html) - GPT-2对话页面

## 数据文件

- [../data/aiml/](../data/aiml/) - AIML规则文件目录
- [../data/models/](../data/models/) - 预训练模型目录
- [../data/training_data/](../data/training_data/) - 训练数据目录
- [../data/knowledge_graph/](../data/knowledge_graph/) - 知识图谱数据目录

## 系统管理

- [../run.py](../run.py) - 应用程序入口
- [../app/__init__.py](../app/__init__.py) - 应用初始化

## 贡献与支持

如需贡献代码或报告问题，请参考[README.md](../README.md)中的贡献指南。

## 文档更新记录

- 2025-05-28: 初始版本
- 2025-05-28: 添加API测试文档
- 2025-05-28: 添加安装指南
- 2025-05-28: 添加发展规划
- 2025-05-29: 整理文档结构，迁移至docs文件夹 