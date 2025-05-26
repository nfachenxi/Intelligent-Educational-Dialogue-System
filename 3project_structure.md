# 智能教育系统项目结构

## 项目概览

该项目是一个基于 Flask 的智能教育系统，集成了 AI 模型、知识图谱和数据分析功能，旨在提供智能化的教育解决方案。

## 目录结构

```
intelligent_edu_system/
├── app/                    # 主应用目录
│   ├── __init__.py         # 应用初始化
│   ├── models/             # 数据模型
│   ├── routes/             # 路由控制器
│   └── utils/              # 工具函数
├── config/                 # 配置文件
│   └── default.py          # 默认配置
├── data/                   # 数据文件
│   └── app.db              # SQLite 数据库
├── docs/                   # 文档
├── migrations/             # 数据库迁移文件
├── tests/                  # 测试用例
├── venv/                   # 虚拟环境
├── manage.py               # 管理脚本
├── requirements.txt        # 依赖包列表
└── run.py                  # 启动脚本
```

## 技术栈

- **Web 框架**: Flask 3.0.2
- **数据库**: SQLAlchemy 2.0.28, Flask-SQLAlchemy 3.1.1
- **认证**: Flask-JWT-Extended 4.6.0
- **AI 模型**: PyTorch 2.2.1, Transformers 4.38.2, AIML 0.9.3
- **知识图谱**: RDFLib 7.0.0
- **数据处理**: NumPy 1.26.4, Pandas 2.2.1, scikit-learn 1.4.1
- **测试工具**: pytest 8.1.1, pytest-cov 4.1.0

## 主要模块

1. **Web 应用层**: Flask 应用及路由控制
2. **数据模型层**: SQLAlchemy ORM 模型
3. **AI 引擎**: 基于 PyTorch 和 Transformers 的智能模型
4. **知识图谱**: 使用 RDFLib 构建的教育知识图谱
5. **工具组件**: 数据处理和分析工具

## Git 忽略策略

项目的 `.gitignore` 文件已配置为忽略以下内容:
- Python 字节码文件和缓存
- 虚拟环境目录
- 数据库文件
- 日志文件
- 本地配置文件
- IDE 相关文件
- AI 模型和大型数据文件
- 临时文件和系统文件 