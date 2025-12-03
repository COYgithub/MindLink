"""
MindLink 文件数据模型

包含：
- SQLAlchemy 数据库模型
- Pydantic 请求/响应模型
- 文件相关的数据验证
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.core.database import Base

# SQLAlchemy 数据库模型
class File(Base):
    """文件数据库模型"""
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True, comment="文件ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="上传用户ID")
    filename = Column(String(255), nullable=False, comment="原始文件名")
    filepath = Column(String(500), nullable=False, comment="存储的文件路径")
    file_size = Column(Integer, nullable=False, comment="文件大小（字节）")
    file_type = Column(String(100), nullable=False, comment="文件类型/ MIME类型")
    file_hash = Column(String(64), nullable=True, index=True, comment="文件哈希值，用于去重")
    description = Column(Text, nullable=True, comment="文件描述")
    is_public = Column(Boolean, default=False, comment="是否公开")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    user = relationship("User", backref="files")
    
    def __repr__(self):
        return f"<File(id={self.id}, filename='{self.filename}', user_id={self.user_id})>"

# Pydantic 请求模型
class FileUploadRequest(BaseModel):
    """文件上传请求模型"""
    description: Optional[str] = Field(None, description="文件描述")
    is_public: Optional[bool] = Field(False, description="是否公开")
    
    class Config:
        json_schema_extra = {
            "example": {
                "description": "项目文档",
                "is_public": False
            }
        }

class FileUpdateRequest(BaseModel):
    """文件更新请求模型"""
    description: Optional[str] = Field(None, description="文件描述")
    is_public: Optional[bool] = Field(None, description="是否公开")
    
    class Config:
        json_schema_extra = {
            "example": {
                "description": "更新的文件描述",
                "is_public": True
            }
        }

# Pydantic 响应模型
class FileResponse(BaseModel):
    """文件信息响应模型"""
    id: int
    user_id: int
    filename: str
    file_size: int
    file_type: str
    description: Optional[str] = None
    is_public: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    download_url: Optional[str] = None  # 下载链接，设为可选以避免转换错误
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "filename": "example.pdf",
                "file_size": 1024000,
                "file_type": "application/pdf",
                "description": "示例文档",
                "is_public": False,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "download_url": "/files/1/download"
            }
        }

class FileListResponse(BaseModel):
    """文件列表响应模型"""
    id: int
    filename: str
    file_size: int
    file_type: str
    created_at: datetime
    download_url: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "filename": "example.pdf",
                "file_size": 1024000,
                "file_type": "application/pdf",
                "created_at": "2024-01-01T00:00:00Z",
                "download_url": "/files/1/download"
            }
        }
