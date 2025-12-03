"""
MindLink 笔记业务逻辑服务

包含：
- 笔记创建、读取、更新、删除
- 笔记版本控制
- 标签管理
- 权限验证
"""

from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import HTTPException, status

from app.models.note import (
    Note, NoteVersion, NoteCreate, NoteUpdate, NoteTagUpdate,
    NoteOut, NoteVersionOut, NoteQueryParams
)
from app.models.user import User
from app.models.common import PaginationInfo, PaginatedResponse
from app.services.ai_service import generate_note_summary

class NoteService:
    """笔记业务逻辑服务类"""
    
    @staticmethod
    def create_note(db: Session, note_create: NoteCreate, current_user: User) -> Note:
        """
        创建新笔记
        
        Args:
            db: 数据库会话
            note_create: 笔记创建请求模型
            current_user: 当前用户
            
        Returns:
            Note: 创建的笔记对象
        """
        # 生成 AI 摘要
        summary = generate_note_summary(note_create.content, note_create.title)
        
        # 创建笔记
        db_note = Note(
            title=note_create.title,
            content=note_create.content,
            summary=summary,
            tags=note_create.tags or [],
            user_id=current_user.id
        )
        
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        
        # 创建初始版本
        initial_version = NoteVersion(
            note_id=db_note.id,
            title=db_note.title,
            content=db_note.content,
            tags=db_note.tags,
            version_number=1,
            change_description="初始版本"
        )
        
        db.add(initial_version)
        db.commit()
        
        return db_note
    
    @staticmethod
    def get_note_by_id(db: Session, note_id: int, current_user: User) -> Note:
        """
        根据ID获取笔记
        
        Args:
            db: 数据库会话
            note_id: 笔记ID
            current_user: 当前用户
            
        Returns:
            Note: 笔记对象
            
        Raises:
            HTTPException: 笔记不存在或权限不足时抛出异常
        """
        db_note = db.query(Note).filter(Note.id == note_id).first()
        
        if not db_note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="笔记不存在"
            )
        
        # 检查权限：只能查看自己的笔记
        if db_note.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足，只能查看自己的笔记"
            )
        
        return db_note
    
    @staticmethod
    def get_notes(
        db: Session, 
        current_user: User,
        query_params: NoteQueryParams
    ) -> PaginatedResponse[NoteOut]:
        """
        获取笔记列表（分页）
        
        Args:
            db: 数据库会话
            current_user: 当前用户
            query_params: 查询参数
            
        Returns:
            PaginatedResponse[NoteOut]: 分页的笔记列表
        """
        # 构建查询
        query = db.query(Note).filter(Note.user_id == current_user.id)
        
        # 标签筛选
        if query_params.tags:
            query = query.filter(Note.tags.overlap(query_params.tags))
        
        # 关键词搜索
        if query_params.search:
            search_term = f"%{query_params.search}%"
            query = query.filter(
                or_(
                    Note.title.ilike(search_term),
                    Note.content.ilike(search_term)
                )
            )
        
        # 用户ID筛选（超级用户可以查看所有用户的笔记）
        if query_params.user_id and current_user.is_superuser:
            query = query.filter(Note.user_id == query_params.user_id)
        
        # 获取总数
        total = query.count()
        
        # 分页
        offset = (query_params.page - 1) * query_params.size
        notes = query.offset(offset).limit(query_params.size).all()
        
        # 计算分页信息
        pages = (total + query_params.size - 1) // query_params.size
        
        pagination_info = PaginationInfo(
            page=query_params.page,
            size=query_params.size,
            total=total,
            pages=pages
        )
        
        return PaginatedResponse[NoteOut](
            items=[NoteOut.from_orm(note) for note in notes],
            pagination=pagination_info
        )
    
    @staticmethod
    def update_note(
        db: Session, 
        note_id: int, 
        note_update: NoteUpdate,
        current_user: User
    ) -> Note:
        """
        更新笔记
        
        Args:
            db: 数据库会话
            note_id: 笔记ID
            note_update: 笔记更新请求模型
            current_user: 当前用户
            
        Returns:
            Note: 更新后的笔记对象
            
        Raises:
            HTTPException: 笔记不存在或权限不足时抛出异常
        """
        # 获取笔记
        db_note = NoteService.get_note_by_id(db, note_id, current_user)
        
        # 获取当前版本号
        current_version = db.query(func.max(NoteVersion.version_number))\
            .filter(NoteVersion.note_id == note_id).scalar() or 0
        
        # 更新笔记信息
        update_data = note_update.dict(exclude_unset=True)
        
        # 记录变更描述
        change_description = update_data.pop("change_description", "更新笔记")
        
        # 执行更新
        for field, value in update_data.items():
            setattr(db_note, field, value)
        
        # 如果内容或标题有更新，重新生成 AI 摘要
        if 'content' in update_data or 'title' in update_data:
            new_summary = generate_note_summary(db_note.content, db_note.title)
            db_note.summary = new_summary
        
        # 创建新版本
        new_version = NoteVersion(
            note_id=db_note.id,
            title=db_note.title,
            content=db_note.content,
            summary=db_note.summary,
            tags=db_note.tags,
            version_number=current_version + 1,
            change_description=change_description
        )
        
        db.add(new_version)
        db.commit()
        db.refresh(db_note)
        
        return db_note
    
    @staticmethod
    def delete_note(db: Session, note_id: int, current_user: User) -> bool:
        """
        删除笔记
        
        Args:
            db: 数据库会话
            note_id: 笔记ID
            current_user: 当前用户
            
        Returns:
            bool: 删除是否成功
            
        Raises:
            HTTPException: 笔记不存在或权限不足时抛出异常
        """
        # 获取笔记
        db_note = NoteService.get_note_by_id(db, note_id, current_user)
        
        try:
            db.delete(db_note)
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="笔记删除失败"
            )
    
    @staticmethod
    def update_note_tags(
        db: Session, 
        note_id: int, 
        tag_update: NoteTagUpdate,
        current_user: User
    ) -> Note:
        """
        更新笔记标签
        
        Args:
            db: 数据库会话
            note_id: 笔记ID
            tag_update: 标签更新请求模型
            current_user: 当前用户
            
        Returns:
            Note: 更新后的笔记对象
        """
        # 获取笔记
        db_note = NoteService.get_note_by_id(db, note_id, current_user)
        
        # 更新标签
        db_note.tags = tag_update.tags
        
        # 创建新版本
        current_version = db.query(func.max(NoteVersion.version_number))\
            .filter(NoteVersion.note_id == note_id).scalar() or 0
        
        new_version = NoteVersion(
            note_id=db_note.id,
            title=db_note.title,
            content=db_note.content,
            tags=db_note.tags,
            version_number=current_version + 1,
            change_description="更新标签"
        )
        
        db.add(new_version)
        db.commit()
        db.refresh(db_note)
        
        return db_note
    
    @staticmethod
    def get_note_versions(
        db: Session, 
        note_id: int, 
        current_user: User
    ) -> List[NoteVersionOut]:
        """
        获取笔记版本历史
        
        Args:
            db: 数据库会话
            note_id: 笔记ID
            current_user: 当前用户
            
        Returns:
            List[NoteVersionOut]: 版本历史列表
        """
        # 检查笔记权限
        NoteService.get_note_by_id(db, note_id, current_user)
        
        # 获取版本历史
        versions = db.query(NoteVersion)\
            .filter(NoteVersion.note_id == note_id)\
            .order_by(NoteVersion.version_number.desc())\
            .all()
        
        return [NoteVersionOut.from_orm(version) for version in versions]
    
    @staticmethod
    def get_note_version(
        db: Session, 
        note_id: int, 
        version_number: int,
        current_user: User
    ) -> NoteVersion:
        """
        获取指定版本的笔记
        
        Args:
            db: 数据库会话
            note_id: 笔记ID
            version_number: 版本号
            current_user: 当前用户
            
        Returns:
            NoteVersion: 指定版本的笔记
            
        Raises:
            HTTPException: 版本不存在时抛出异常
        """
        # 检查笔记权限
        NoteService.get_note_by_id(db, note_id, current_user)
        
        # 获取指定版本
        version = db.query(NoteVersion)\
            .filter(
                and_(
                    NoteVersion.note_id == note_id,
                    NoteVersion.version_number == version_number
                )
            ).first()
        
        if not version:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定版本不存在"
            )
        
        return version
    
    @staticmethod
    def restore_note_version(
        db: Session, 
        note_id: int, 
        version_number: int,
        current_user: User
    ) -> Note:
        """
        恢复笔记到指定版本
        
        Args:
            db: 数据库会话
            note_id: 笔记ID
            version_number: 要恢复的版本号
            current_user: 当前用户
            
        Returns:
            Note: 恢复后的笔记对象
        """
        # 获取指定版本
        version = NoteService.get_note_version(db, note_id, version_number, current_user)
        
        # 获取当前笔记
        db_note = NoteService.get_note_by_id(db, note_id, current_user)
        
        # 恢复内容
        db_note.title = version.title
        db_note.content = version.content
        db_note.tags = version.tags
        
        # 创建新版本
        current_version = db.query(func.max(NoteVersion.version_number))\
            .filter(NoteVersion.note_id == note_id).scalar() or 0
        
        new_version = NoteVersion(
            note_id=db_note.id,
            title=db_note.title,
            content=db_note.content,
            tags=db_note.tags,
            version_number=current_version + 1,
            change_description=f"恢复到版本 {version_number}"
        )
        
        db.add(new_version)
        db.commit()
        db.refresh(db_note)
        
        return db_note
    
    @staticmethod
    def get_user_tags(db: Session, current_user: User) -> List[str]:
        """
        获取用户的所有标签
        
        Args:
            db: 数据库会话
            current_user: 当前用户
            
        Returns:
            List[str]: 标签列表
        """
        # 查询用户所有笔记的标签
        result = db.query(Note.tags)\
            .filter(Note.user_id == current_user.id)\
            .all()
        
        # 合并所有标签并去重
        all_tags = set()
        for tags in result:
            if tags[0]:  # tags[0] 是 ARRAY 字段
                all_tags.update(tags[0])
        
        return sorted(list(all_tags))
    
    @staticmethod
    def search_notes(
        db: Session, 
        current_user: User,
        query: str,
        tags: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[NoteOut]:
        """
        搜索笔记
        
        Args:
            db: 数据库会话
            current_user: 当前用户
            query: 搜索关键词
            tags: 标签筛选
            limit: 限制返回数量
            
        Returns:
            List[NoteOut]: 搜索结果列表
        """
        # 构建搜索查询
        search_query = db.query(Note).filter(Note.user_id == current_user.id)
        
        # 标签筛选
        if tags:
            search_query = search_query.filter(Note.tags.overlap(tags))
        
        # 关键词搜索
        if query:
            search_term = f"%{query}%"
            search_query = search_query.filter(
                or_(
                    Note.title.ilike(search_term),
                    Note.content.ilike(search_term)
                )
            )
        
        # 按更新时间排序并限制数量
        notes = search_query.order_by(Note.updated_at.desc()).limit(limit).all()
        
        return [NoteOut.from_orm(note) for note in notes] 