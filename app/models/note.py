"""
MindLink 笔记数据模型

包含：
- SQLAlchemy 数据库模型（Note、NoteVersion）
- Pydantic 请求/响应模型
- 笔记相关的数据验证
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, ARRAY, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.core.database import Base

# SQLAlchemy 数据库模型
class Note(Base):
    """笔记数据库模型"""
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True, comment="笔记ID")
    title = Column(String(200), nullable=False, comment="笔记标题")
    content = Column(Text, nullable=False, comment="笔记内容（Markdown格式）")
    summary = Column(Text, nullable=True, comment="AI生成的摘要")
    tags = Column(JSON, default=list, comment="标签列表")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="作者ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    user = relationship("User", back_populates="notes")
    versions = relationship("NoteVersion", back_populates="note", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Note(id={self.id}, title='{self.title}', user_id={self.user_id})>"

class NoteVersion(Base):
    """笔记版本历史模型"""
    __tablename__ = "note_versions"
    
    id = Column(Integer, primary_key=True, index=True, comment="版本ID")
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False, comment="笔记ID")
    title = Column(String(200), nullable=False, comment="版本标题")
    content = Column(Text, nullable=False, comment="版本内容")
    summary = Column(Text, nullable=True, comment="版本摘要")
    tags = Column(JSON, default=list, comment="版本标签")
    version_number = Column(Integer, nullable=False, comment="版本号")
    change_description = Column(String(500), nullable=True, comment="变更描述")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="版本创建时间")
    
    # 关联关系
    note = relationship("Note", back_populates="versions")
    
    def __repr__(self):
        return f"<NoteVersion(id={self.id}, note_id={self.note_id}, version={self.version_number})>"

# Pydantic 请求模型
class NoteCreate(BaseModel):
    """笔记创建请求模型"""
    title: str = Field(..., min_length=1, max_length=200, description="笔记标题")
    content: str = Field(..., description="笔记内容")  # 移除min_length限制以更好地支持特殊字符
    tags: Optional[List[str]] = Field(default=[], description="标签列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "我的第一篇笔记",
                "content": "# 欢迎使用 MindLink\n\n这是一个支持 Markdown 的笔记系统。",
                "tags": ["介绍", "Markdown"]
            }
        }
        # 允许特殊字符和换行符正确处理
        allow_population_by_field_name = True
        json_encoders = {
            str: lambda v: v  # 确保字符串直接传递，不进行额外编码处理
        }

class NoteUpdate(BaseModel):
    """笔记更新请求模型"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="笔记标题")
    content: Optional[str] = Field(None, description="笔记内容")  # 移除min_length限制以更好地支持特殊字符
    tags: Optional[List[str]] = Field(None, description="标签列表")
    change_description: Optional[str] = Field(None, max_length=500, description="变更描述")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "更新后的标题",
                "content": "# 更新后的内容\n\n内容已经更新。",
                "tags": ["更新", "Markdown"],
                "change_description": "更新了标题和内容"
            }
        }
        # 允许特殊字符和换行符正确处理
        allow_population_by_field_name = True
        json_encoders = {
            str: lambda v: v  # 确保字符串直接传递，不进行额外编码处理
        }

class NoteTagUpdate(BaseModel):
    """笔记标签更新请求模型"""
    tags: List[str] = Field(..., description="新的标签列表")
    
    class Config:
        json_schema_extra  = {
            "example": {
                "tags": ["新标签1", "新标签2", "新标签3"]
            }
        }

# Pydantic 响应模型
class NoteOut(BaseModel):
    """笔记信息响应模型"""
    id: int
    title: str
    content: str
    summary: Optional[str] = None
    tags: List[str]
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_schema_extra  = {
            "example": {
                "id": 1,
                "title": "我的第一篇笔记",
                "content": "# 欢迎使用 MindLink\n\n这是一个支持 Markdown 的笔记系统。",
                "summary": "介绍 MindLink 笔记系统",
                "tags": ["介绍", "Markdown"],
                "user_id": 1,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }

class NoteWithUser(NoteOut):
    """包含用户信息的笔记响应模型"""
    user: dict  # 用户基本信息
    
    class Config:
        from_attributes = True

class NoteVersionOut(BaseModel):
    """笔记版本信息响应模型"""
    id: int
    note_id: int
    title: str
    content: str
    summary: Optional[str] = None
    tags: List[str]
    version_number: int
    change_description: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra  = {
            "example": {
                "id": 1,
                "note_id": 1,
                "title": "我的第一篇笔记",
                "content": "# 欢迎使用 MindLink\n\n这是一个支持 Markdown 的笔记系统。",
                "summary": "介绍 MindLink 笔记系统",
                "tags": ["介绍", "Markdown"],
                "version_number": 1,
                "change_description": "初始版本",
                "created_at": "2024-01-01T00:00:00Z"
            }
        }

# 查询参数模型
class NoteQueryParams(BaseModel):
    """笔记查询参数模型"""
    page: int = Field(default=1, ge=1, description="页码")
    size: int = Field(default=20, ge=1, le=100, description="每页大小")
    tags: Optional[List[str]] = Field(default=None, description="标签筛选")
    search: Optional[str] = Field(default=None, description="搜索关键词")
    user_id: Optional[int] = Field(default=None, description="用户ID筛选")
    
    class Config:
        json_schema_extra  = {
            "example": {
                "page": 1,
                "size": 20,
                "tags": ["技术", "Python"],
                "search": "FastAPI",
                "user_id": 1
            }
        }

# 分页响应模型
class PaginatedResponse(BaseModel):
    """分页响应模型"""
    items: List[NoteOut]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        json_schema_extra  = {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "size": 20,
                "pages": 5
            }
        } 