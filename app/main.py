"""
MindLink 个人知识管理平台 - 主应用入口

此文件是 FastAPI 应用的主入口点，负责：
- 创建 FastAPI 应用实例
- 配置 CORS、中间件
- 注册 API 路由
- 配置异常处理器
- 设置文档路径
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
import logging
from datetime import datetime

# 导入路由模块
# from app.api.v1 import api_router
from app.api.auth import auth_router
from app.api.notes import notes_router
from app.api.files import files_router

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用实例
app = FastAPI(
    title="MindLink - 个人知识管理平台",
    description="基于 FastAPI 的智能知识管理系统，支持 Markdown 笔记、AI 摘要和版本控制",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI 文档路径
    redoc_url="/redoc",    # ReDoc 文档路径
    openapi_url="/openapi.json"  # OpenAPI 规范文件路径
)

# 配置 CORS 中间件
# 允许跨域请求，支持前端应用访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # 开发环境前端
        "http://localhost:8080",      # 开发环境前端（备用端口）
        "https://yourdomain.com",     # 生产环境域名（需要替换）
    ],
    allow_credentials=True,           # 允许携带认证信息
    allow_methods=["*"],             # 允许所有 HTTP 方法
    allow_headers=["*"],             # 允许所有请求头
)

# 配置可信主机中间件
# 防止 HTTP Host 头攻击
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "127.0.0.1",
        "yourdomain.com",            # 生产环境域名（需要替换）
    ]
)

# 全局异常处理器
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """处理 HTTP 异常"""
    logger.error("HTTP 异常: {} - {}".format(exc.status_code, exc.detail))
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理请求验证异常"""
    logger.error("请求验证异常: {}".format(exc.errors()))
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "请求数据验证失败",
            "details": exc.errors(),
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """处理通用异常"""
    logger.error("未处理的异常: {}".format(str(exc)), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "服务器内部错误",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# 健康检查端点
@app.get("/health", tags=["系统"])
async def health_check():
    """系统健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "MindLink API",
        "version": "1.0.0"
    }

# 根路径
@app.get("/", tags=["系统"])
async def root():
    """API 根路径"""
    return {
        "message": "欢迎使用 MindLink 个人知识管理平台",
        "version": "1.0.0",
        "docs": "/docs",
        "timestamp": datetime.utcnow().isoformat()
    }

# 注册 API 路由
# 注意：路由的注册顺序很重要，更具体的路由应该先注册
app.include_router(auth_router, prefix="/auth", tags=["认证"])
app.include_router(notes_router, prefix="/notes", tags=["笔记"])
app.include_router(files_router, prefix="/files", tags=["文件"])

# 应用启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行的操作"""
    logger.info("MindLink 应用正在启动...")
    # 这里可以添加数据库连接、Redis 连接等初始化代码

# 应用关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行的操作"""
    logger.info("MindLink 应用正在关闭...")
    # 这里可以添加资源清理代码

if __name__ == "__main__":
    # 开发环境直接运行
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",           # 监听所有网络接口
        port=8000,                 # 端口号
        reload=True,               # 开发模式：代码变更时自动重载
        log_level="info"           # 日志级别
    ) 