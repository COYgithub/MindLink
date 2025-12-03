# MindLink Docker 部署指南

本文档介绍如何使用 Docker 和 Docker Compose 部署 MindLink 个人知识管理平台。

## 🐳 环境要求

- Docker Engine 20.10+
- Docker Compose 2.0+
- 至少 2GB 可用内存
- 至少 10GB 可用磁盘空间

## 🚀 快速开始

### 1. 环境配置

复制环境变量模板文件：

```bash
cp env.example .env
```

编辑 `.env` 文件，配置必要的环境变量：

```bash
# 必需配置
SECRET_KEY=your-super-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here

# 可选配置（使用默认值）
ENVIRONMENT=production
BUILD_TARGET=production
```

### 2. 开发环境部署

使用开发环境配置启动服务：

```bash
# 构建并启动开发环境
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f app
```

开发环境特点：
- 代码热重载支持
- 详细的调试日志
- 开发工具（git, vim）
- 代码目录挂载

### 3. 生产环境部署

使用生产环境配置启动服务：

```bash
# 构建并启动生产环境
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f app
```

生产环境特点：
- 多进程工作模式
- 资源限制和监控
- 优化的系统依赖
- 包含 Nginx 反向代理

## 🏗️ 多阶段构建

### 开发阶段构建

```bash
# 构建开发镜像
docker build --target development -t mindlink:dev .

# 运行开发容器
docker run -d -p 8000:8000 mindlink:dev
```

### 生产阶段构建

```bash
# 构建生产镜像
docker build --target production -t mindlink:prod .

# 运行生产容器
docker run -d -p 8000:8000 mindlink:prod
```

## 🔧 服务配置

### 应用服务 (app)

- **端口**: 8000 (可配置)
- **环境变量**: 支持通过 `.env` 文件配置
- **健康检查**: 每30秒检查一次
- **资源限制**: 内存 1GB，CPU 1核

### 数据库服务 (db)

- **类型**: PostgreSQL 15
- **端口**: 5432 (可配置)
- **数据持久化**: `postgres_data` 卷
- **健康检查**: 每10秒检查一次

### 缓存服务 (redis)

- **类型**: Redis 7
- **端口**: 6379 (可配置)
- **数据持久化**: `redis_data` 卷
- **内存限制**: 256MB
- **健康检查**: 每10秒检查一次

### 反向代理 (nginx)

- **端口**: 80 (HTTP), 443 (HTTPS)
- **配置**: 仅在生产环境启动
- **SSL**: 支持自定义证书

## 📊 监控和日志

### 健康检查

所有服务都配置了健康检查：

```bash
# 查看服务健康状态
docker-compose ps

# 手动检查健康状态
docker-compose exec app curl -f http://localhost:8000/health
```

### 日志管理

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs -f app
docker-compose logs -f db
docker-compose logs -f redis

# 查看最近100行日志
docker-compose logs --tail=100 app
```

### 资源监控

```bash
# 查看容器资源使用情况
docker stats

# 查看特定容器资源使用
docker stats mindlink-app mindlink-db mindlink-redis
```

## 🔒 安全配置

### 环境变量

敏感信息通过环境变量配置：

```bash
# 数据库密码
POSTGRES_PASSWORD=your-db-password

# Redis 密码
REDIS_PASSWORD=your-redis-password

# JWT 密钥
SECRET_KEY=your-jwt-secret

# OpenAI API 密钥
OPENAI_API_KEY=your-openai-key
```

### 网络隔离

- 所有服务运行在自定义网络 `mindlink-network`
- 子网: 172.20.0.0/16
- 服务间通过服务名通信

### 用户权限

- 应用以非 root 用户 `appuser` 运行
- 数据库和缓存服务使用专用用户

## 📈 扩展和优化

### 水平扩展

```bash
# 扩展应用服务实例
docker-compose up -d --scale app=3

# 扩展数据库（需要配置主从复制）
docker-compose up -d --scale db=2
```

### 负载均衡

使用 Nginx 进行负载均衡：

```nginx
upstream mindlink_app {
    server app:8000;
    server app2:8000;
    server app3:8000;
}
```

### 性能优化

- **数据库连接池**: 配置连接池大小和超时
- **Redis 缓存**: 配置内存策略和过期策略
- **应用缓存**: 启用 FastAPI 缓存中间件

## 🚨 故障排除

### 常见问题

1. **服务启动失败**
   ```bash
   # 查看详细错误信息
   docker-compose logs app
   
   # 检查环境变量
   docker-compose config
   ```

2. **数据库连接失败**
   ```bash
   # 检查数据库状态
   docker-compose exec db pg_isready -U mindlink_user
   
   # 检查网络连接
   docker-compose exec app ping db
   ```

3. **内存不足**
   ```bash
   # 调整资源限制
   # 编辑 docker-compose.yml 中的 deploy.resources
   ```

### 调试模式

启用调试模式获取更多信息：

```bash
# 设置环境变量
export DEBUG=true
export LOG_LEVEL=DEBUG

# 重新启动服务
docker-compose down
docker-compose up -d
```

## 🔄 更新和升级

### 应用更新

```bash
# 拉取最新代码
git pull origin main

# 重新构建镜像
docker-compose build --no-cache

# 重启服务
docker-compose up -d
```

### 数据库迁移

```bash
# 运行数据库迁移
docker-compose exec app alembic upgrade head

# 检查迁移状态
docker-compose exec app alembic current
```

### 备份和恢复

```bash
# 备份数据库
docker-compose exec db pg_dump -U mindlink_user mindlink_db > backup.sql

# 恢复数据库
docker-compose exec -T db psql -U mindlink_user mindlink_db < backup.sql
```

## 📚 相关文档

- [FastAPI 部署指南](https://fastapi.tiangolo.com/deployment/)
- [Docker Compose 参考](https://docs.docker.com/compose/)
- [PostgreSQL Docker 镜像](https://hub.docker.com/_/postgres)
- [Redis Docker 镜像](https://hub.docker.com/_/redis)

## 🤝 支持和反馈

如果在部署过程中遇到问题，请：

1. 检查本文档的故障排除部分
2. 查看项目的 GitHub Issues
3. 联系项目维护者

---

**注意**: 生产环境部署前，请务必：
- 修改所有默认密码
- 配置 SSL 证书
- 设置防火墙规则
- 配置监控和告警
- 制定备份策略 