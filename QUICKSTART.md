venv# MindLink 快速启动指南

## 🚀 快速开始

### 1. 环境准备

确保您的系统已安装：
- Python 3.8+
- pip 包管理器

### 2. 克隆项目

```bash
git clone <repository-url>
cd MindLink
```

### 3. 检查 poetry 版本

```bash
poetry --version
```
初始化 poetry
```bash
poetry init
```

关联本地 python 环境，最好是 venv

```bash
# Windows
poetry env use "D:\software\python venv\python3.10.11\python.exe"
```
确认 Poetry 使用的是指定虚拟环境：
```bash
poetry env info
```
### 4. 安装依赖
配置国内源，在当前项目的 pyproject.toml 的最后添加
```bash
[[tool.poetry.source]]
name = "aliyun"
url = "https://mirrors.aliyun.com/pypi/simple/"
priority = "primary"
```
**一定要在 poetry shell 中执行命令**
poetry install --verbose
### 5. 初始化数据库
```bash
python init_db.py
```

这将：
- 创建 SQLite 数据库文件
- 创建所有必要的表
- 创建默认超级用户（admin/admin123）

### 7. 启动应用

```bash
# 使用启动脚本
python run.py

# 或直接使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 8. 访问应用

- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **根路径**: http://localhost:8000/

## 🔐 默认账户

开发环境会自动创建超级用户：

- **用户名**: admin
- **邮箱**: admin@mindlink.com
- **密码**: admin123

**⚠️ 重要**: 生产环境请务必修改默认密码！

## 📚 API 使用示例

### 用户注册

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 用户登录

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 创建笔记

```bash
curl -X POST "http://localhost:8000/notes/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "我的第一篇笔记",
    "content": "# 欢迎使用 MindLink\n\n这是一个支持 Markdown 的笔记系统。",
    "tags": ["介绍", "Markdown"]
  }'
```

### 获取笔记列表

```bash
curl -X GET "http://localhost:8000/notes/?page=1&size=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🐳 Docker 部署

### 使用 Docker Compose

```bash
# 构建和启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f app

# 停止服务
docker-compose down
```

### 环境变量配置

创建 `.env` 文件：

```env
ENVIRONMENT=production
SECRET_KEY=your-super-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=postgresql://mindlink_user:mindlink_password@db:5432/mindlink_db
REDIS_URL=redis://redis:6379
```

## 🔧 开发模式

### 启用调试

```bash
# 设置环境变量
export DEBUG=true
export SQL_ECHO=true

# 或修改 .env 文件
DEBUG=true
SQL_ECHO=true
```

### 热重载

```bash
python run.py --reload
```

### 自定义端口

```bash
python run.py --port 9000
```

## 📝 项目结构

```
MindLink/
├── app/                    # 应用主目录
│   ├── api/               # API 路由
│   │   ├── auth/         # 认证相关
│   │   └── notes/        # 笔记相关
│   ├── core/             # 核心配置
│   ├── models/           # 数据模型
│   ├── services/         # 业务逻辑
│   └── utils/            # 工具函数
├── requirements.txt       # 依赖包
├── init_db.py            # 数据库初始化
├── run.py                # 启动脚本
└── README.md             # 详细文档
```

## 🚨 常见问题

### 1. 端口被占用

```bash
# 使用其他端口
python run.py --port 9000
```

### 2. 数据库连接失败

- 检查 `.env` 文件中的 `DATABASE_URL`
- 确保数据库服务正在运行
- 检查数据库权限

### 3. 依赖安装失败

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 4. 权限错误

- Windows: 以管理员身份运行
- Linux/Mac: 检查文件权限

## 📞 获取帮助

- 查看 [README.md](README.md) 获取详细文档
- 检查 [API 文档](http://localhost:8000/docs) 了解所有端点
- 提交 Issue 报告问题

## 🎯 下一步

1. 熟悉 API 接口
2. 开发前端应用
3. 配置生产环境
4. 添加更多功能模块

---

**Happy Coding! 🎉** 