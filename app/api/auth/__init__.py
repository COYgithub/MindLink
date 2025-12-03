"""
MindLink 认证 API 包

用户认证相关的路由和端点
"""

from fastapi import APIRouter

# 创建认证路由器
auth_router = APIRouter()

# 导入和注册所有的认证路由
from .auth import router as auth_endpoints

auth_router.include_router(auth_endpoints) 