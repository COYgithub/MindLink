"""
MindLink 认证 API 路由

包含：
- 用户注册
- 用户登录
- 令牌刷新
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import UserCreate, UserLogin, UserOut, Token, UserUpdate
from app.models.common import SuccessResponse, ErrorResponse
from app.services.user_service import UserService
from app.utils.auth import get_current_user, User

# 创建认证路由器
router = APIRouter()

@router.post("/register", response_model=SuccessResponse, tags=["认证"])
async def register_user(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """
    用户注册
    
    - **username**: 用户名（3-50字符）
    - **email**: 邮箱地址
    - **password**: 密码（最少6字符）
    """
    try:
        # 创建用户
        user = UserService.create_user(db, user_create)
        
        return SuccessResponse(
            code=201,
            message="用户注册成功",
            data={
                "user": UserOut.from_orm(user),
                "message": "请使用注册的凭据登录"
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="用户注册失败"
        )

@router.post("/login", response_model=SuccessResponse, tags=["认证"])
async def login_user(
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    """
    用户登录
    
    - **username**: 用户名或邮箱
    - **password**: 密码
    """
    try:
        # 验证用户凭据
        auth_result = UserService.authenticate_user_login(db, user_login)
        
        return SuccessResponse(
            code=200,
            message="登录成功",
            data=auth_result
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录失败"
        )

@router.post("/refresh", response_model=SuccessResponse, tags=["认证"])
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    刷新访问令牌
    
    - **refresh_token**: 刷新令牌
    """
    try:
        from app.utils.auth import refresh_access_token
        
        # 刷新访问令牌
        new_access_token = refresh_access_token(refresh_token)
        
        return SuccessResponse(
            code=200,
            message="令牌刷新成功",
            data={
                "access_token": new_access_token,
                "token_type": "bearer"
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="令牌刷新失败"
        )

@router.get("/me", response_model=SuccessResponse, tags=["认证"])
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户信息
    
    需要有效的访问令牌
    """
    return SuccessResponse(
        code=200,
        message="获取用户信息成功",
        data=UserOut.from_orm(current_user)
    )

@router.post("/logout", response_model=SuccessResponse, tags=["认证"])
async def logout_user(
    current_user: User = Depends(get_current_user)
):
    """
    用户登出
    
    注意：JWT 是无状态的，客户端需要删除本地存储的令牌
    """
    return SuccessResponse(
        code=200,
        message="登出成功",
        data={
            "message": "请删除本地存储的访问令牌"
        }
    )

@router.put("/profile", response_model=SuccessResponse, tags=["认证"])
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新用户资料
    
    - **username**: 新用户名（可选）
    - **email**: 新邮箱（可选）
    - **password**: 新密码（可选）
    """
    try:
        # 更新用户信息
        updated_user = UserService.update_user(
            db, current_user.id, user_update, current_user
        )
        
        return SuccessResponse(
            code=200,
            message="用户资料更新成功",
            data=UserOut.from_orm(updated_user)
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="用户资料更新失败"
        )

@router.delete("/account", response_model=SuccessResponse, tags=["认证"])
async def delete_user_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除用户账户
    
    注意：此操作不可逆，将删除用户的所有数据
    """
    try:
        # 删除用户账户
        UserService.delete_user(db, current_user.id, current_user)
        
        return SuccessResponse(
            code=200,
            message="账户删除成功",
            data={
                "message": "您的账户已被永久删除"
            }
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="账户删除失败"
        ) 