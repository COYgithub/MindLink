"""
MindLink 笔记 API 包

笔记管理相关的路由和端点
"""

from fastapi import APIRouter

# 创建笔记路由器
notes_router = APIRouter()

# 导入和注册所有的笔记路由
from .notes import router as notes_endpoints

notes_router.include_router(notes_endpoints) 