"""
MindLink 通用数据模型

包含：
- 统一响应格式
- 分页模型
- 异常模型
"""

from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any
from enum import Enum

# 响应状态枚举
class ResponseStatus(str, Enum):
    """响应状态枚举"""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"

# 通用响应模型
class BaseResponse(BaseModel):
    """基础响应模型"""
    code: int = Field(200, description="响应状态码")
    message: str = Field("操作成功", description="响应消息")
    status: ResponseStatus = Field(ResponseStatus.SUCCESS, description="响应状态")

class SuccessResponse(BaseResponse):
    """成功响应模型"""
    data: Optional[Any] = Field(None, description="响应数据")
    
    class Config:
        json_schema_extra  = {
            "example": {
                "code": 200,
                "message": "操作成功",
                "status": "success",
                "data": None
            }
        }

class ErrorResponse(BaseResponse):
    """错误响应模型"""
    error_code: Optional[str] = Field(None, description="错误代码")
    details: Optional[Any] = Field(None, description="错误详情")
    
    class Config:
        json_schema_extra  = {
            "example": {
                "code": 400,
                "message": "请求参数错误",
                "status": "error",
                "error_code": "INVALID_PARAMS",
                "details": "字段验证失败"
            }
        }

# 分页模型
class PaginationInfo(BaseModel):
    """分页信息模型"""
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页大小")
    total: int = Field(..., description="总记录数")
    pages: int = Field(..., description="总页数")
    
    @property
    def has_next(self) -> bool:
        """是否有下一页"""
        return self.page < self.pages
    
    @property
    def has_prev(self) -> bool:
        """是否有上一页"""
        return self.page > 1
    
    @property
    def offset(self) -> int:
        """偏移量"""
        return (self.page - 1) * self.size

# 泛型分页响应模型
T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    items: list[T] = Field(..., description="数据列表")
    pagination: PaginationInfo = Field(..., description="分页信息")
    
    class Config:
        json_schema_extra  = {
            "example": {
                "items": [],
                "pagination": {
                    "page": 1,
                    "size": 20,
                    "total": 100,
                    "pages": 5
                }
            }
        }

# 健康检查响应模型
class HealthCheckResponse(BaseResponse):
    """健康检查响应模型"""
    data: dict = Field(..., description="健康状态信息")
    
    class Config:
        json_schema_extra  = {
            "example": {
                "code": 200,
                "message": "服务正常",
                "status": "success",
                "data": {
                    "status": "healthy",
                    "timestamp": "2024-01-01T00:00:00Z",
                    "service": "MindLink API",
                    "version": "1.0.0"
                }
            }
        }

# 统计信息响应模型
class StatisticsResponse(BaseResponse):
    """统计信息响应模型"""
    data: dict = Field(..., description="统计信息")
    
    class Config:
        json_schema_extra  = {
            "example": {
                "code": 200,
                "message": "获取统计信息成功",
                "status": "success",
                "data": {
                    "total_users": 100,
                    "total_notes": 500,
                    "total_tags": 50,
                    "active_users_today": 25
                }
            }
        }

# 批量操作响应模型
class BatchOperationResponse(BaseResponse):
    """批量操作响应模型"""
    data: dict = Field(..., description="批量操作结果")
    
    class Config:
        json_schema_extra  = {
            "example": {
                "code": 200,
                "message": "批量操作成功",
                "status": "success",
                "data": {
                    "total": 100,
                    "success": 95,
                    "failed": 5,
                    "failed_items": ["item1", "item2"]
                }
            }
        }

# 文件上传响应模型
class FileUploadResponse(BaseResponse):
    """文件上传响应模型"""
    data: dict = Field(..., description="文件上传结果")
    
    class Config:
        json_schema_extra  = {
            "example": {
                "code": 200,
                "message": "文件上传成功",
                "status": "success",
                "data": {
                    "filename": "example.jpg",
                    "size": 1024,
                    "url": "/uploads/example.jpg",
                    "mime_type": "image/jpeg"
                }
            }
        }

# 搜索响应模型
class SearchResponse(BaseResponse):
    """搜索响应模型"""
    data: dict = Field(..., description="搜索结果")
    
    class Config:
        json_schema_extra  = {
            "example": {
                "code": 200,
                "message": "搜索完成",
                "status": "success",
                "data": {
                    "query": "FastAPI",
                    "total_results": 25,
                    "results": [],
                    "suggestions": ["FastAPI", "Fast API", "Fast-API"]
                }
            }
        } 