# 智能教育对话系统安装指南

本文档提供了智能教育对话系统的详细安装和配置说明。

## 系统要求

### 硬件要求
- CPU: 2核或以上
- 内存: 4GB或以上
- 存储: 1GB可用空间
- 网络: 互联网连接（用于下载依赖和模型）

### 软件要求
- 操作系统: Windows 10+, macOS 10.15+, 或 Linux (Ubuntu 18.04+)
- Python: 3.8+
- SQLite: 3.0+
- Git: 2.0+

## 安装步骤

### 1. 准备环境

#### Windows系统
1. 安装Python 3.8+
   - 从 [Python官网](https://www.python.org/downloads/) 下载并安装
   - 安装时勾选"Add Python to PATH"
   - 验证安装: `python --version`

2. 安装Git
   - 从 [Git官网](https://git-scm.com/download/win) 下载并安装
   - 验证安装: `git --version`

#### Linux系统 (Ubuntu)
```bash
# 更新包列表
sudo apt update

# 安装Python和pip
sudo apt install python3.8 python3-pip python3-venv

# 安装Git
sudo apt install git

# 安装SQLite
sudo apt install sqlite3

# 验证安装
python3 --version
git --version
sqlite3 --version
```

#### macOS系统
```bash
# 使用Homebrew安装
brew install python
brew install git
brew install sqlite

# 验证安装
python3 --version
git --version
sqlite3 --version
```

### 2. 获取项目代码

```bash
# 克隆代码库
git clone https://github.com/your-username/intelligent_edu_system.git
cd intelligent_edu_system
```

### 3. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

依赖项包括：
- Flask==3.0.2
- Flask-SQLAlchemy==3.1.1
- Flask-Migrate==4.0.5
- Flask-JWT-Extended==4.6.0
- Flask-Cors==4.0.0
- SQLAlchemy==2.0.28
- python-aiml==0.9.3
- transformers==4.38.2
- torch==2.2.1
- nltk==3.8.1
- spacy==3.7.2
- rdflib==7.0.0
- pytest==8.1.1

### 5. 配置应用

#### 5.1 基本配置

创建或修改`.env`文件（项目根目录下）:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URI=sqlite:///app.db
JWT_SECRET_KEY=your-jwt-secret-key
```

替换`your-secret-key-here`和`your-jwt-secret-key`为安全的随机字符串。

#### 5.2 模型配置

GPT-2模型默认使用模拟模式。如需使用真实模型，请修改`run.py`文件中的`init_gpt2(use_mock=True)`为`init_gpt2(use_mock=False)`。

#### 5.3 目录结构准备

确保数据目录存在：

```bash
# 创建AIML规则目录
mkdir -p data/aiml

# 创建模型目录
mkdir -p data/models/gpt2

# 创建训练数据目录
mkdir -p data/training_data

# 创建知识图谱目录
mkdir -p data/knowledge_graph
```

### 6. 初始化数据库

```bash
# 初始化迁移仓库
flask db init

# 创建迁移脚本
flask db migrate -m "Initial migration"

# 应用迁移
flask db upgrade
```

### 7. 运行应用

```bash
python run.py
```

应用将在 http://127.0.0.1:5000 启动。

## 可选配置

### HTTPS支持

对于生产环境，建议配置HTTPS：

1. 生成SSL证书
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

2. 修改`run.py`
```python
if __name__ == '__main__':
    app.run(
        debug=False,
        host='0.0.0.0',
        port=5000,
        ssl_context=('cert.pem', 'key.pem')
    )
```

### 日志配置

可以在`app/__init__.py`中修改日志配置：

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
```

### 代理设置

如果您在使用代理网络，需要设置环境变量：

```bash
# Windows
set HTTP_PROXY=http://proxy-server:port
set HTTPS_PROXY=http://proxy-server:port

# Linux/macOS
export HTTP_PROXY=http://proxy-server:port
export HTTPS_PROXY=http://proxy-server:port
```

## 常见问题排查

### 安装依赖失败

**问题**: `pip install -r requirements.txt`失败

**解决方案**:
1. 尝试更新pip: `pip install --upgrade pip`
2. 单独安装问题包: `pip install package-name`
3. 检查是否需要额外的系统依赖（如C编译器）

### 数据库迁移错误

**问题**: 执行`flask db migrate`时出错

**解决方案**:
1. 删除migrations文件夹和instance/app.db文件
2. 重新执行`flask db init`、`flask db migrate`和`flask db upgrade`

### 模型加载错误

**问题**: GPT-2模型加载失败

**解决方案**:
1. 确认是否有网络连接问题
2. 检查SSL证书问题，尝试设置环境变量: `PYTHONHTTPSVERIFY=0`
3. 使用模拟模式: 在`run.py`中设置`use_mock=True`

### AIML规则加载问题

**问题**: AIML规则文件加载失败

**解决方案**:
1. 检查data/aiml目录是否存在
2. 检查XML文件是否格式正确
3. 检查编码是否为UTF-8

### 端口被占用

**问题**: 启动应用时提示端口5000已被占用

**解决方案**:
1. 找到并关闭占用端口5000的进程
2. 或修改`run.py`中的端口号: `port=5001`

## 升级指南

当需要升级系统时，请按照以下步骤操作：

1. 备份数据
```bash
cp -r instance/app.db instance/app.db.backup
```

2. 拉取最新代码
```bash
git pull origin main
```

3. 更新依赖
```bash
pip install -r requirements.txt --upgrade
```

4. 更新数据库
```bash
flask db migrate -m "Update migration"
flask db upgrade
```

5. 重启应用
```bash
python run.py
```

## 支持与反馈

如果您在安装过程中遇到任何问题，请通过以下方式获取支持：

- 提交GitHub Issue
- 发送邮件到support@example.com
- 查阅[常见问题文档](faq.md) 