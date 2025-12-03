"""
MindLink 用户业务逻辑服务

包含：
- 用户注册
- 用户登录
- 用户信息管理
- 用户权限验证
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.user import User, UserCreate, UserUpdate, UserOut, UserLogin
from app.utils.auth import get_password_hash, authenticate_user, generate_tokens
from app.models.common import SuccessResponse, ErrorResponse

class UserService:
    """用户业务逻辑服务类"""
    
    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """
        创建新用户
        
        Args:
            db: 数据库会话
            user_create: 用户创建请求模型
            
        Returns:
            User: 创建的用户对象
            
        Raises:
            HTTPException: 用户名或邮箱已存在时抛出异常
        """
        try:
            # 检查用户名是否已存在
            existing_user = db.query(User).filter(User.username == user_create.username).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="用户名已存在"
                )
            
            # 检查邮箱是否已存在
            existing_email = db.query(User).filter(User.email == user_create.email).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已被注册"
                )
            
            # 创建新用户
            hashed_password = get_password_hash(user_create.password)
            db_user = User(
                username=user_create.username,
                email=user_create.email,
                hashed_password=hashed_password,
                is_active=True,
                is_superuser=False
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            return db_user
            
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户创建失败，请检查输入数据"
            )
    
    @staticmethod
    def authenticate_user_login(db: Session, user_login: UserLogin) -> dict:
        """
        用户登录认证
        
        Args:
            db: 数据库会话
            user_login: 用户登录请求模型
            
        Returns:
            dict: 包含令牌的认证信息
            
        Raises:
            HTTPException: 用户名或密码错误时抛出异常
        """
        user = authenticate_user(db, user_login.username, user_login.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户账户已停用"
            )
        
        # 生成令牌
        tokens = generate_tokens(user)
        
        return {
            "user": UserOut.from_orm(user),
            "tokens": tokens
        }
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        根据ID获取用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            Optional[User]: 用户对象，不存在时返回None
        """
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """
        根据用户名获取用户
        
        Args:
            db: 数据库会话
            username: 用户名
            
        Returns:
            Optional[User]: 用户对象，不存在时返回None
        """
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        根据邮箱获取用户
        
        Args:
            db: 数据库会话
            email: 邮箱地址
            
        Returns:
            Optional[User]: 用户对象，不存在时返回None
        """
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_users(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        active_only: bool = True
    ) -> List[User]:
        """
        获取用户列表
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 限制返回的记录数
            active_only: 是否只返回活跃用户
            
        Returns:
            List[User]: 用户列表
        """
        query = db.query(User)
        
        if active_only:
            query = query.filter(User.is_active == True)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_user(
        db: Session, 
        user_id: int, 
        user_update: UserUpdate,
        current_user: User
    ) -> User:
        """
        更新用户信息
        
        Args:
            db: 数据库会话
            user_id: 要更新的用户ID
            user_update: 用户更新请求模型
            current_user: 当前操作用户
            
        Returns:
            User: 更新后的用户对象
            
        Raises:
            HTTPException: 权限不足或用户不存在时抛出异常
        """
        # 检查权限：只能更新自己的信息，或超级用户可以更新任何用户
        if current_user.id != user_id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足，只能更新自己的信息"
            )
        
        # 获取要更新的用户
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 更新用户信息
        update_data = user_update.dict(exclude_unset=True)
        
        # 如果更新密码，需要重新加密
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # 检查用户名唯一性
        if "username" in update_data and update_data["username"] != db_user.username:
            existing_user = db.query(User).filter(User.username == update_data["username"]).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="用户名已存在"
                )
        
        # 检查邮箱唯一性
        if "email" in update_data and update_data["email"] != db_user.email:
            existing_email = db.query(User).filter(User.email == update_data["email"]).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已被注册"
                )
        
        # 执行更新
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        try:
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户信息更新失败"
            )
    
    @staticmethod
    def delete_user(db: Session, user_id: int, current_user: User) -> bool:
        """
        删除用户
        
        Args:
            db: 数据库会话
            user_id: 要删除的用户ID
            current_user: 当前操作用户
            
        Returns:
            bool: 删除是否成功
            
        Raises:
            HTTPException: 权限不足或用户不存在时抛出异常
        """
        # 检查权限：只能删除自己的账户，或超级用户可以删除任何用户
        if current_user.id != user_id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足，只能删除自己的账户"
            )
        
        # 获取要删除的用户
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 不能删除超级用户
        if db_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不能删除超级用户账户"
            )
        
        try:
            db.delete(db_user)
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="用户删除失败"
            )
    
    @staticmethod
    def deactivate_user(db: Session, user_id: int, current_user: User) -> User:
        """
        停用用户账户
        
        Args:
            db: 数据库会话
            user_id: 要停用的用户ID
            current_user: 当前操作用户
            
        Returns:
            User: 停用后的用户对象
            
        Raises:
            HTTPException: 权限不足或用户不存在时抛出异常
        """
        # 检查权限：超级用户可以停用任何用户
        if not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
        
        # 获取要停用的用户
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 不能停用超级用户
        if db_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不能停用超级用户账户"
            )
        
        db_user.is_active = False
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def activate_user(db: Session, user_id: int, current_user: User) -> User:
        """
        激活用户账户
        
        Args:
            db: 数据库会话
            user_id: 要激活的用户ID
            current_user: 当前操作用户
            
        Returns:
            User: 激活后的用户对象
            
        Raises:
            HTTPException: 权限不足或用户不存在时抛出异常
        """
        # 检查权限：超级用户可以激活任何用户
        if not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
        
        # 获取要激活的用户
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        db_user.is_active = True
        db.commit()
        db.refresh(db_user)
        
        return db_user 