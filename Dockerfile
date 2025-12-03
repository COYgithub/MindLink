# ==================== 第一阶段：构建前端（Vue.js） ====================
FROM node:20-alpine AS frontend-builder

# 设置工作目录
WORKDIR /app/frontend

# 设置 npm 国内镜像源
RUN npm config set registry https://registry.npmmirror.com

# 复制前端依赖文件
COPY frontend/package.json frontend/package-lock.json* ./
# 安装前端依赖
RUN npm install

# 复制前端代码
COPY frontend/ .

# 构建前端静态文件
RUN npm run build

# ==================== 第二阶段：构建后端（FastAPI） ====================
FROM python:3.9-slim AS backend-builder

# 设置工作目录
WORKDIR /app

# 安装 Poetry
RUN pip install --no-cache-dir poetry==1.8.3 -i https://mirrors.aliyun.com/pypi/simple/

# 复制后端依赖文件
COPY pyproject.toml ./

# 配置 Poetry 并安装依赖（不使用锁文件）
RUN poetry config virtualenvs.create false \
    && poetry config repositories.aliyun https://mirrors.aliyun.com/pypi/simple/ \
    && poetry install --only main --no-interaction

# 复制后端代码（假设在 app 目录）
COPY app/ ./app/

# ==================== 最终阶段：运行环境 ====================
FROM python:3.9-slim

# 安装运行时依赖（如 psycopg2 的系统依赖）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 从构建阶段复制 Python 包
COPY --from=backend-builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=backend-builder /usr/local/bin/ /usr/local/bin/

# 复制后端代码
COPY --from=backend-builder /app/app/ ./app/

# 复制前端构建的静态文件
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# 暴露端口
EXPOSE 8000

# 启动 FastAPI 应用（假设主应用文件为 app/main.py）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]