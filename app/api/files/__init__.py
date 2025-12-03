"""
MindLink 文件 API 路由初始化

此模块创建并导出文件相关的 API 路由器
"""

from fastapi import APIRouter

# 创建文件路由器
files_router = APIRouter()

# 导入并注册文件端点
from .files import *
