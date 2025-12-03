# MindLink - 个人知识管理平台

基于 FastAPI 的智能知识管理系统，支持 Markdown 笔记、AI 摘要和版本控制。

## 🚀 核心功能

- **用户认证系统**：JWT 令牌认证，支持注册、登录
- **Markdown 笔记管理**：完整的 CRUD 操作，支持标签和分类
- **AI 辅助摘要**：集成 OpenAI API，自动生成笔记摘要
- **版本控制**：笔记修改历史追踪和回滚
- **标签系统**：灵活的标签管理和搜索
- **RESTful API**：完整的 API 接口，支持前端集成

## 🛠️ 技术栈

### 后端
- **FastAPI** - 现代、快速的 Web 框架
- **SQLAlchemy** - Python ORM 框架
- **Pydantic** - 数据验证和序列化
- **JWT** - 用户认证和授权
- **bcrypt** - 密码加密

### 数据库
- **SQLite** - 开发环境（默认）
- **PostgreSQL** - 生产环境

### 缓存
- **Redis** - 会话存储和缓存

### AI 服务
- **OpenAI API** - 智能摘要生成

### 部署
- **Docker** - 容器化部署
- **Docker Compose** - 多服务编排

## 📁 项目结构

```
MindLink/
├── app/                    # 应用主目录
│   ├── api/               # API 路由
│   │   ├── v1/           # API 版本 1
│   │   ├── auth/         # 认证相关路由
│   │   └── notes/        # 笔记相关路由
│   ├── core/             # 核心配置
│   │   ├── config.py     # 应用配置
│   │   └── database.py   # 数据库配置
│   ├── models/           # 数据模型
│   ├── services/         # 业务逻辑服务
│   ├── utils/            # 工具函数
│   └── tests/            # 测试文件
├── requirements.txt       # Python 依赖
├── Dockerfile            # Docker 镜像构建
├── docker-compose.yml    # Docker 服务编排
├── env.example           # 环境变量示例
└── README.md             # 项目说明
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Docker 和 Docker Compose（可选）
- Redis（可选，用于缓存）

### 本地开发

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd MindLink
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate     # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   ```bash
   cp env.example .env
   # 编辑 .env 文件，配置必要的环境变量
   ```

5. **运行应用**
   ```bash
   python -m app.main
   # 或
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **访问应用**
   - API 文档：http://localhost:8000/docs
   - 健康检查：http://localhost:8000/health

### Docker 部署

1. **构建和启动服务**
   ```bash
   docker-compose up -d
   ```

2. **查看服务状态**
   ```bash
   docker-compose ps
   ```

3. **查看日志**
   ```bash
   docker-compose logs -f app
   ```

4. **停止服务**
   ```bash
   docker-compose down
   ```

## ⚙️ 配置说明

### 环境变量

主要配置项说明：

- `ENVIRONMENT`: 运行环境（development/staging/production）
- `DATABASE_URL`: 数据库连接字符串
- `SECRET_KEY`: JWT 签名密钥
- `OPENAI_API_KEY`: OpenAI API 密钥
- `REDIS_URL`: Redis 连接地址

### 数据库配置

- **开发环境**：默认使用 SQLite，数据文件为 `mindlink.db`
- **生产环境**：推荐使用 PostgreSQL，通过 `DATABASE_URL` 配置

### 安全配置

- JWT 令牌过期时间可配置
- 密码使用 bcrypt 加密
- 支持 CORS 配置
- 可信主机验证

## 📚 API 文档

启动应用后，访问以下地址查看 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### 主要端点

- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录
- `GET /notes` - 获取笔记列表
- `POST /notes` - 创建新笔记
- `GET /notes/{id}` - 获取笔记详情
- `PUT /notes/{id}` - 更新笔记
- `DELETE /notes/{id}` - 删除笔记

## 🔧 开发指南

### 添加新功能

1. 在 `app/models/` 中定义数据模型
2. 在 `app/services/` 中实现业务逻辑
3. 在 `app/api/` 中添加路由
4. 在 `app/tests/` 中编写测试

### 代码规范

- 使用类型注解
- 遵循 PEP 8 代码风格
- 编写详细的文档字符串
- 添加适当的错误处理

### 测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest app/tests/test_notes.py

# 生成覆盖率报告
pytest --cov=app --cov-report=html
```

## 🚀 部署

### 生产环境

1. 设置 `ENVIRONMENT=production`
2. 配置 PostgreSQL 数据库
3. 配置 Redis 缓存
4. 设置强密码的 `SECRET_KEY`
5. 配置域名和 SSL 证书
6. 使用 Docker Compose 或 Kubernetes 部署

### 性能优化

- 启用 Redis 缓存
- 配置数据库连接池
- 使用 CDN 加速静态资源
- 启用 Gzip 压缩

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献流程

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

如有问题或建议，请：

- 提交 [Issue](../../issues)
- 发送邮件至：support@mindlink.com
- 加入讨论群：[Discord](https://discord.gg/mindlink)

## 🙏 致谢

感谢以下开源项目的支持：

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [OpenAI](https://openai.com/)
- [Redis](https://redis.io/)

---

**MindLink** - 让知识管理更智能 🧠✨ 