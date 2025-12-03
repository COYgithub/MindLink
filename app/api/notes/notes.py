"""
MindLink 笔记 API 路由

包含：
- 笔记 CRUD 操作
- 标签管理
- 版本控制
- 搜索功能
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.note import (
    NoteCreate, NoteUpdate, NoteTagUpdate, NoteOut, NoteVersionOut,
    NoteQueryParams, PaginatedResponse
)
from app.models.common import SuccessResponse
from app.services.note_service import NoteService
from app.utils.auth import get_current_user, User

# 创建笔记路由器
router = APIRouter()

@router.post("/", response_model=SuccessResponse, tags=["笔记"])
async def create_note(
    note_create: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建新笔记
    
    - **title**: 笔记标题
    - **content**: 笔记内容（Markdown格式）
    - **tags**: 标签列表（可选）
    """
    try:
        # 创建笔记
        note = NoteService.create_note(db, note_create, current_user)
        
        return SuccessResponse(
            code=201,
            message="笔记创建成功",
            data=NoteOut.from_orm(note)
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="笔记创建失败"
        )

@router.get("/", response_model=SuccessResponse, tags=["笔记"])
async def get_notes(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页大小"),
    tags: Optional[List[str]] = Query(None, description="标签筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    user_id: Optional[int] = Query(None, description="用户ID筛选"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取笔记列表（分页）
    
    - **page**: 页码（从1开始）
    - **size**: 每页大小（1-100）
    - **tags**: 标签筛选（可选）
    - **search**: 搜索关键词（可选）
    - **user_id**: 用户ID筛选（可选，仅超级用户可用）
    """
    try:
        # 构建查询参数
        query_params = NoteQueryParams(
            page=page,
            size=size,
            tags=tags,
            search=search,
            user_id=user_id
        )
        
        # 获取笔记列表
        result = NoteService.get_notes(db, current_user, query_params)
        
        return SuccessResponse(
            code=200,
            message="获取笔记列表成功",
            data=result
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取笔记列表失败"
        )

@router.get("/{note_id}", response_model=SuccessResponse, tags=["笔记"])
async def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取笔记详情
    
    - **note_id**: 笔记ID
    """
    try:
        # 获取笔记
        note = NoteService.get_note_by_id(db, note_id, current_user)
        
        return SuccessResponse(
            code=200,
            message="获取笔记详情成功",
            data=NoteOut.from_orm(note)
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取笔记详情失败"
        )

@router.put("/{note_id}", response_model=SuccessResponse, tags=["笔记"])
async def update_note(
    note_id: int,
    note_update: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新笔记
    
    - **note_id**: 笔记ID
    - **title**: 新标题（可选）
    - **content**: 新内容（可选）
    - **tags**: 新标签列表（可选）
    - **change_description**: 变更描述（可选）
    """
    try:
        # 更新笔记
        note = NoteService.update_note(db, note_id, note_update, current_user)
        
        return SuccessResponse(
            code=200,
            message="笔记更新成功",
            data=NoteOut.from_orm(note)
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="笔记更新失败"
        )

@router.delete("/{note_id}", response_model=SuccessResponse, tags=["笔记"])
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除笔记
    
    - **note_id**: 笔记ID
    
    注意：此操作不可逆，将删除笔记及其所有版本历史
    """
    try:
        # 删除笔记
        NoteService.delete_note(db, note_id, current_user)
        
        return SuccessResponse(
            code=200,
            message="笔记删除成功",
            data={
                "message": "笔记已被永久删除"
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="笔记删除失败"
        )

@router.post("/{note_id}/tags", response_model=SuccessResponse, tags=["笔记"])
async def update_note_tags(
    note_id: int,
    tag_update: NoteTagUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新笔记标签
    
    - **note_id**: 笔记ID
    - **tags**: 新的标签列表
    """
    try:
        # 更新标签
        note = NoteService.update_note_tags(db, note_id, tag_update, current_user)
        
        return SuccessResponse(
            code=200,
            message="标签更新成功",
            data=NoteOut.from_orm(note)
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="标签更新失败"
        )

@router.get("/{note_id}/versions", response_model=SuccessResponse, tags=["笔记"])
async def get_note_versions(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取笔记版本历史
    
    - **note_id**: 笔记ID
    """
    try:
        # 获取版本历史
        versions = NoteService.get_note_versions(db, note_id, current_user)
        
        return SuccessResponse(
            code=200,
            message="获取版本历史成功",
            data=versions
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取版本历史失败"
        )

@router.get("/{note_id}/versions/{version_number}", response_model=SuccessResponse, tags=["笔记"])
async def get_note_version(
    note_id: int,
    version_number: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取指定版本的笔记
    
    - **note_id**: 笔记ID
    - **version_number**: 版本号
    """
    try:
        # 获取指定版本
        version = NoteService.get_note_version(db, note_id, version_number, current_user)
        
        return SuccessResponse(
            code=200,
            message="获取指定版本成功",
            data=NoteVersionOut.from_orm(version)
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取指定版本失败"
        )

@router.post("/{note_id}/versions/{version_number}/restore", response_model=SuccessResponse, tags=["笔记"])
async def restore_note_version(
    note_id: int,
    version_number: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    恢复笔记到指定版本
    
    - **note_id**: 笔记ID
    - **version_number**: 要恢复的版本号
    
    注意：此操作将创建一个新的版本记录
    """
    try:
        # 恢复版本
        note = NoteService.restore_note_version(db, note_id, version_number, current_user)
        
        return SuccessResponse(
            code=200,
            message="版本恢复成功",
            data=NoteOut.from_orm(note)
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="版本恢复失败"
        )

@router.get("/tags/all", response_model=SuccessResponse, tags=["笔记"])
async def get_user_tags(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户的所有标签
    """
    try:
        # 获取用户标签
        tags = NoteService.get_user_tags(db, current_user)
        
        return SuccessResponse(
            code=200,
            message="获取标签列表成功",
            data=tags
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取标签列表失败"
        )

@router.get("/search", response_model=SuccessResponse, tags=["笔记"])
async def search_notes(
    query: str = Query(..., description="搜索关键词"),
    tags: Optional[List[str]] = Query(None, description="标签筛选"),
    limit: int = Query(50, ge=1, le=200, description="限制返回数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    搜索笔记
    
    - **query**: 搜索关键词
    - **tags**: 标签筛选（可选）
    - **limit**: 限制返回数量（1-200）
    """
    try:
        # 搜索笔记
        notes = NoteService.search_notes(db, current_user, query, tags, limit)
        
        return SuccessResponse(
            code=200,
            message="搜索完成",
            data={
                "query": query,
                "tags": tags,
                "total_results": len(notes),
                "results": notes
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="搜索失败"
        ) 