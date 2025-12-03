"""
MindLink 数据模型包

包含所有的数据库模型和 Pydantic 模型
"""

# 导入所有模型
from .user import (
    User, UserCreate, UserUpdate, UserOut, UserInDB, 
    UserLogin, Token, TokenData
)

from .note import (
    Note, NoteVersion, NoteCreate, NoteUpdate, NoteTagUpdate,
    NoteOut, NoteWithUser, NoteVersionOut, NoteQueryParams
)

from .common import (
    BaseResponse, SuccessResponse, ErrorResponse, ResponseStatus,
    PaginationInfo, PaginatedResponse, HealthCheckResponse,
    StatisticsResponse, BatchOperationResponse, FileUploadResponse,
    SearchResponse
)

# 导出所有模型
__all__ = [
    # 用户相关模型
    "User", "UserCreate", "UserUpdate", "UserOut", "UserInDB",
    "UserLogin", "Token", "TokenData",
    
    # 笔记相关模型
    "Note", "NoteVersion", "NoteCreate", "NoteUpdate", "NoteTagUpdate",
    "NoteOut", "NoteWithUser", "NoteVersionOut", "NoteQueryParams",
    
    # 通用模型
    "BaseResponse", "SuccessResponse", "ErrorResponse", "ResponseStatus",
    "PaginationInfo", "PaginatedResponse", "HealthCheckResponse",
    "StatisticsResponse", "BatchOperationResponse", "FileUploadResponse",
    "SearchResponse"
] 