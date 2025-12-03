"""
MindLink 文件处理服务

负责文件的核心业务逻辑：
- 文件上传和保存
- 文件下载和访问控制
- 文件列表和详情获取
- 文件更新和删除
- 文件哈希计算和去重
"""

import os
import hashlib
import uuid
from typing import List, Dict, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status, UploadFile
import logging

from app.models.file import File, FileUploadRequest, FileUpdateRequest
from app.models.user import User
from app.core.config import get_settings

# 获取配置
settings = get_settings()

# 配置日志
logger = logging.getLogger(__name__)

# 从配置文件获取允许的文件扩展名
ALLOWED_EXTENSIONS = set[str](settings.ALLOWED_FILE_EXTENSIONS.split(","))

class FileService:
    """文件服务类"""
    
    @staticmethod
    def get_upload_dir() -> str:
        """获取文件上传目录"""
        # 从配置中获取上传目录
        upload_dir = settings.UPLOAD_DIR
        
        # 确保目录存在
        os.makedirs(upload_dir, exist_ok=True)
        return upload_dir
    
    @staticmethod
    def calculate_file_hash(file_content: bytes) -> str:
        """计算文件哈希值（用于去重）"""
        # 从配置中获取哈希算法
        if settings.FILE_HASH_ALGORITHM == "sha256":
            hash_obj = hashlib.sha256()
        elif settings.FILE_HASH_ALGORITHM == "md5":
            hash_obj = hashlib.md5()
        elif settings.FILE_HASH_ALGORITHM == "sha1":
            hash_obj = hashlib.sha1()
        else:
            # 默认使用sha256
            hash_obj = hashlib.sha256()
        
        hash_obj.update(file_content)
        return hash_obj.hexdigest()
    
    @staticmethod
    def validate_file(file: UploadFile, max_size: Optional[int] = None) -> None:
        """验证文件是否符合要求"""
        # 使用配置中的最大文件大小
        if max_size is None:
            max_size = settings.MAX_FILE_SIZE
        
        # 检查文件大小
        if file.size and file.size > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"文件大小超过限制，最大允许 {max_size / (1024 * 1024)}MB"
            )
        
        # 检查文件扩展名
        if file.filename:
            file_ext = file.filename.split(".")[-1].lower()
            if file_ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"不支持的文件类型：.{file_ext}"
                )
    
    @staticmethod
    def generate_filepath(upload_dir: str, original_filename: str, user_id: int) -> str:
        """生成唯一的文件存储路径"""
        # 按用户ID创建子目录
        user_dir = os.path.join(upload_dir, str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        
        # 生成唯一文件名，保留原始扩展名
        file_ext = ""
        if original_filename and "." in original_filename:
            file_ext = "." + original_filename.split(".")[-1].lower()
        
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        return os.path.join(user_dir, unique_filename)
    
    @staticmethod
    async def save_upload_file(file: UploadFile, filepath: str) -> Dict[str, Any]:
        """保存上传的文件到磁盘"""
        try:
            # 读取文件内容
            content = await file.read()
            
            # 验证文件大小
            file_size = len(content)
            if file_size > settings.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"文件大小超过限制，最大允许 {settings.MAX_FILE_SIZE / (1024 * 1024)}MB"
                )
            
            # 计算文件哈希
            file_hash = FileService.calculate_file_hash(content)
            
            # 写入文件
            with open(filepath, "wb") as buffer:
                buffer.write(content)
            
            return {
                "file_size": file_size,
                "file_hash": file_hash,
                "filepath": filepath
            }
        except Exception as e:
            logger.error(f"保存文件失败: {str(e)}")
            # 如果文件已创建，删除它
            if os.path.exists(filepath):
                os.remove(filepath)
            raise
    
    @staticmethod
    async def upload_file(db: Session, user: User, file: UploadFile, file_request: FileUploadRequest) -> File:
        """上传文件并创建记录"""
        try:
            # 验证文件
            FileService.validate_file(file)
            
            # 获取上传目录
            upload_dir = FileService.get_upload_dir()
            
            # 生成文件路径
            filepath = FileService.generate_filepath(upload_dir, file.filename, user.id)
            
            # 保存文件
            file_info = await FileService.save_upload_file(file, filepath)
            
            # 检查用户文件数量限制
            user_file_count = db.query(File).filter(File.user_id == user.id).count()
            if user_file_count >= settings.MAX_FILES_PER_USER:
                # 删除临时文件
                if os.path.exists(file_info["filepath"]):
                    os.remove(file_info["filepath"])
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"文件数量超过限制，最大允许 {settings.MAX_FILES_PER_USER} 个文件"
                )
            
            # 检查用户存储容量限制
            user_total_size = db.query(func.sum(File.file_size)).filter(File.user_id == user.id).scalar() or 0
            if user_total_size + file_info["file_size"] > settings.MAX_STORAGE_PER_USER:
                # 删除临时文件
                if os.path.exists(file_info["filepath"]):
                    os.remove(file_info["filepath"])
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"存储空间超过限制，已使用 {user_total_size / (1024 * 1024 * 1024):.2f}GB，最大允许 {settings.MAX_STORAGE_PER_USER / (1024 * 1024 * 1024)}GB"
                )
            
            # 检查是否已存在相同文件（如果启用了重复检查）
            if settings.ENABLE_FILE_DUPLICATE_CHECK:
                existing_file = db.query(File).filter(
                    File.file_hash == file_info["file_hash"],
                    File.user_id == user.id
                ).first()
                
                if existing_file and existing_file.id is not None:
                    # 可以选择使用现有文件或保持新文件，这里选择保持新文件
                    pass
            
            # 创建文件记录
            db_file = File(
                user_id=user.id,
                filename=file.filename,
                filepath=file_info["filepath"],
                file_size=file_info["file_size"],
                file_type=file.content_type or "application/octet-stream",
                file_hash=file_info["file_hash"],
                description=file_request.description,
                is_public=file_request.is_public
            )
            
            db.add(db_file)
            db.commit()
            db.refresh(db_file)
            
            logger.info(f"用户 {user.id} 上传文件: {file.filename}, 存储路径: {filepath}")
            return db_file
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"上传文件失败: {str(e)}")
            raise
    
    @staticmethod
    def get_user_files(db: Session, user_id: int, skip: int = 0, limit: int = 20) -> List[File]:
        """获取用户的文件列表"""
        try:
            files = db.query(File).filter(
                File.user_id == user_id
            ).order_by(File.created_at.desc()).offset(skip).limit(limit).all()
            return files
        except Exception as e:
            logger.error(f"获取用户文件列表失败: {str(e)}")
            raise
    
    @staticmethod
    def get_public_files(db: Session, skip: int = 0, limit: int = 20) -> List[File]:
        """获取公开文件列表"""
        try:
            files = db.query(File).filter(
                File.is_public == True
            ).order_by(File.created_at.desc()).offset(skip).limit(limit).all()
            return files
        except Exception as e:
            logger.error(f"获取公开文件列表失败: {str(e)}")
            raise
    
    @staticmethod
    def get_file_detail(db: Session, file_id: int, current_user: Optional[User]) -> File:
        """获取文件详情，包含权限检查"""
        # 获取文件
        file = db.query(File).filter(File.id == file_id).first()
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )
        
        # 权限检查：文件公开或当前用户是上传者
        if not file.is_public and (not current_user or current_user.id != file.user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限访问此文件"
            )
        
        return file
    
    @staticmethod
    def get_file_for_download(db: Session, file_id: int, current_user: Optional[User]) -> Dict[str, str]:
        """获取文件下载信息，包含权限检查"""
        # 获取文件
        file = FileService.get_file_detail(db, file_id, current_user)
        
        # 检查文件是否存在
        if not os.path.exists(file.filepath):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在或已被删除"
            )
        
        return {
            "filepath": file.filepath,
            "filename": file.filename,
            "file_type": file.file_type
        }
    
    @staticmethod
    def update_file(db: Session, file_id: int, file_update: FileUpdateRequest, current_user: User) -> File:
        """更新文件信息"""
        # 获取文件
        file = db.query(File).filter(File.id == file_id).first()
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )
        
        # 权限检查：只有上传者可以更新
        if file.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限更新此文件"
            )
        
        # 更新文件信息
        update_data = file_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(file, field, value)
        
        file.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(file)
        
        logger.info(f"用户 {current_user.id} 更新文件 {file_id} 信息")
        return file
    
    @staticmethod
    def delete_file(db: Session, file_id: int, current_user: User) -> None:
        """删除文件"""
        # 获取文件
        file = db.query(File).filter(File.id == file_id).first()
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )
        
        # 权限检查：只有上传者可以删除
        if file.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限删除此文件"
            )
        
        # 记录文件路径用于删除
        filepath = file.filepath
        
        # 从数据库中删除
        db.delete(file)
        db.commit()
        
        # 从磁盘中删除文件
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"从磁盘删除文件: {filepath}")
        except Exception as e:
            # 文件删除失败，记录日志但不回滚数据库操作
            logger.error(f"删除磁盘文件失败: {str(e)}")
        
        logger.info(f"用户 {current_user.id} 删除文件: {file_id}")
    
    @staticmethod
    def clean_empty_directories() -> None:
        """清理空目录（定期调用）"""
        upload_dir = FileService.get_upload_dir()
        try:
            for root, dirs, files in os.walk(upload_dir, topdown=False):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
                        logger.info(f"清理空目录: {dir_path}")
        except Exception as e:
            logger.error(f"清理空目录失败: {str(e)}")
