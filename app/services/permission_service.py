"""
MindLink 权限服务

负责处理应用中的权限控制，特别是文件上传相关的权限验证：
- 文件所有权验证
- 公开文件访问控制
- 用户权限级别检查
"""

from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.models.user import User
from app.models.file import File

# 配置日志
logger = logging.getLogger(__name__)


class PermissionService:
    """权限服务类"""
    
    @staticmethod
    def check_file_ownership(
        db: Session,
        file_id: int,
        user: User,
        allow_superuser: bool = True
    ) -> File:
        """
        检查文件所有权
        
        Args:
            db: 数据库会话
            file_id: 文件ID
            user: 当前用户
            allow_superuser: 是否允许超级用户访问任何文件
            
        Returns:
            File: 文件对象
            
        Raises:
            HTTPException: 文件不存在或用户无权访问时抛出异常
        """
        # 查找文件
        file = db.query(File).filter(File.id == file_id).first()
        
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )
        
        # 检查所有权
        is_owner = file.user_id == user.id
        is_admin = allow_superuser and user.is_superuser
        is_public = file.is_public
        
        # 只有文件所有者、超级用户或公开文件可以访问
        if not is_owner and not is_admin and not is_public:
            logger.warning(
                f"用户 {user.username} 尝试访问不属于自己的文件 {file_id}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您无权访问此文件"
            )
        
        return file
    
    @staticmethod
    def check_file_modification_permission(
        db: Session,
        file_id: int,
        user: User,
        allow_superuser: bool = True
    ) -> File:
        """
        检查文件修改权限（比读取权限更严格，只允许所有者和超级用户修改）
        
        Args:
            db: 数据库会话
            file_id: 文件ID
            user: 当前用户
            allow_superuser: 是否允许超级用户修改任何文件
            
        Returns:
            File: 文件对象
            
        Raises:
            HTTPException: 文件不存在或用户无权修改时抛出异常
        """
        # 查找文件
        file = db.query(File).filter(File.id == file_id).first()
        
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )
        
        # 检查所有权或超级用户权限
        is_owner = file.user_id == user.id
        is_admin = allow_superuser and user.is_superuser
        
        # 只有文件所有者或超级用户可以修改文件
        if not is_owner and not is_admin:
            logger.warning(
                f"用户 {user.username} 尝试修改不属于自己的文件 {file_id}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您无权修改此文件"
            )
        
        return file
    
    @staticmethod
    def can_access_public_files(user: User) -> bool:
        """
        检查用户是否可以访问公开文件
        
        Args:
            user: 用户对象
            
        Returns:
            bool: 是否有权访问公开文件
        """
        # 默认所有已激活用户都可以访问公开文件
        return user.is_active
    
    @staticmethod
    def can_upload_files(user: User) -> bool:
        """
        检查用户是否有权限上传文件
        
        Args:
            user: 用户对象
            
        Returns:
            bool: 是否有权上传文件
            
        Raises:
            HTTPException: 用户无权上传文件时抛出异常
        """
        # 检查用户是否激活
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您的账户已停用，无法上传文件"
            )
        
        # 这里可以添加更多的权限检查，例如：
        # - 检查用户是否有特定角色
        # - 检查用户是否有上传配额
        # - 检查用户是否在允许上传的时间内
        
        return True
    
    @staticmethod
    def can_share_files(user: User, file: File) -> bool:
        """
        检查用户是否可以分享指定文件
        
        Args:
            user: 用户对象
            file: 文件对象
            
        Returns:
            bool: 是否可以分享文件
        """
        # 只有文件所有者或超级用户可以分享文件
        return file.user_id == user.id or user.is_superuser
