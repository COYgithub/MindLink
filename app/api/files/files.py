"""
MindLink 文件上传/下载 API 路由

包含：
- 文件上传
- 文件下载
- 文件列表获取
- 文件详情获取
- 文件删除
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from app.core.database import get_db
from app.models.file import FileUploadRequest, FileUpdateRequest, FileResponse, FileListResponse
from app.models.common import SuccessResponse
from app.services.file_service import FileService
from app.services.permission_service import PermissionService
from app.utils.auth import get_current_user, User
from app.api.files import files_router

@files_router.post("/upload", response_model=SuccessResponse, tags=["文件"])
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    is_public: Optional[bool] = Form(False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    上传文件
    
    - **file**: 要上传的文件
    - **description**: 文件描述（可选）
    - **is_public**: 是否公开文件（默认：否）
    """
    try:
        # 检查上传权限
        PermissionService.can_upload_files(current_user)
        
        # 创建文件上传请求对象
        file_request = FileUploadRequest(
            description=description,
            is_public=is_public
        )
        
        # 上传文件（添加await关键字处理异步调用）
        uploaded_file = await FileService.upload_file(db, current_user, file, file_request)
        
        # 构建响应 - 使用字典转换而非直接使用from_orm，确保正确设置download_url
        file_dict = {
            "id": uploaded_file.id,
            "user_id": uploaded_file.user_id,
            "filename": uploaded_file.filename,
            "file_size": uploaded_file.file_size,
            "file_type": uploaded_file.file_type,
            "description": uploaded_file.description,
            "is_public": uploaded_file.is_public,
            "created_at": uploaded_file.created_at,
            "updated_at": uploaded_file.updated_at,
            "download_url": f"/files/{uploaded_file.id}/download"
        }
        response_data = FileResponse(**file_dict)
        
        return SuccessResponse(
            code=201,
            message="文件上传成功",
            data=response_data
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件上传失败: {str(e)}"
        )

@files_router.get("/download/{file_id}", tags=["文件"])
async def download_file(
    file_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    下载文件
    
    - file_id: 文件ID
    
    权限：
    - 公开文件：所有人可下载
    - 非公开文件：只有上传者可下载
    """
    try:
        # 使用权限服务检查文件访问权限
        if current_user:
            # 已认证用户使用权限服务检查
            file = PermissionService.check_file_ownership(db, file_id, current_user)
            # 获取文件路径
            file_path = file.filepath
            filename = file.filename
            content_type = file.file_type
        else:
            # 未认证用户只允许访问公开文件
            file_info = FileService.get_file_for_download(db, file_id, None)
            file_path = file_info["filepath"]
            filename = file_info["filename"]
            content_type = file_info["file_type"]
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在"
            )
        
        # 返回文件响应
        return FastAPIFileResponse(
            path=file_path,
            filename=filename,
            media_type=content_type or "application/octet-stream"
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件下载失败: {str(e)}"
        )

@files_router.get("/", response_model=SuccessResponse, tags=["文件"])
async def get_files(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取文件列表
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    
    返回当前用户的所有文件
    """
    try:
        # 获取文件列表
        files = FileService.get_user_files(db, current_user.id, skip, limit)
        
        # 构建响应数据 - 使用字典转换确保正确设置download_url
        response_data = []
        for file in files:
            file_dict = {
                "id": file.id,
                "filename": file.filename,
                "file_size": file.file_size,
                "file_type": file.file_type,
                "created_at": file.created_at,
                "download_url": f"/files/{file.id}/download"
            }
            file_list = FileListResponse(**file_dict)
            response_data.append(file_list)
        
        return SuccessResponse(
            code=200,
            message="获取文件列表成功",
            data={
                "files": response_data,
                "total": len(response_data),
                "skip": skip,
                "limit": limit
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取文件列表失败: {str(e)}"
        )

@files_router.get("/public", response_model=SuccessResponse, tags=["文件"])
async def get_public_files(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    获取公开文件列表
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的最大记录数
    
    不需要认证即可访问
    """
    try:
        # 获取公开文件列表
        files = FileService.get_public_files(db, skip, limit)
        
        # 构建响应数据 - 使用字典转换确保正确设置download_url
        response_data = []
        for file in files:
            file_dict = {
                "id": file.id,
                "filename": file.filename,
                "file_size": file.file_size,
                "file_type": file.file_type,
                "created_at": file.created_at,
                "download_url": f"/files/{file.id}/download"
            }
            file_list = FileListResponse(**file_dict)
            response_data.append(file_list)
        
        return SuccessResponse(
            code=200,
            message="获取公开文件列表成功",
            data={
                "files": response_data,
                "total": len(response_data),
                "skip": skip,
                "limit": limit
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取公开文件列表失败: {str(e)}"
        )

@files_router.get("/{file_id}", response_model=SuccessResponse, tags=["文件"])
async def get_file_detail(
    file_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取文件详情
    
    - **file_id**: 文件ID
    
    权限：
    - 公开文件：所有人可查看
    - 非公开文件：只有上传者可查看
    """
    try:
        # 使用权限服务检查文件访问权限
        if current_user:
            # 已认证用户使用权限服务检查
            file = PermissionService.check_file_ownership(db, file_id, current_user)
        else:
            # 未认证用户只允许访问公开文件
            file = FileService.get_file_detail(db, file_id, None)
        
        # 构建响应 - 使用字典转换确保正确设置download_url
        file_dict = {
            "id": file.id,
            "user_id": file.user_id,
            "filename": file.filename,
            "file_size": file.file_size,
            "file_type": file.file_type,
            "description": file.description,
            "is_public": file.is_public,
            "created_at": file.created_at,
            "updated_at": file.updated_at,
            "download_url": f"/files/{file.id}/download"
        }
        response_data = FileResponse(**file_dict)
        
        return SuccessResponse(
            code=200,
            message="获取文件详情成功",
            data=response_data
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取文件详情失败: {str(e)}"
        )

@files_router.put("/{file_id}", response_model=SuccessResponse, tags=["文件"])
async def update_file(
    file_id: int,
    file_update: FileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新文件信息
    
    - **file_id**: 文件ID
    - **description**: 新的文件描述（可选）
    - **is_public**: 是否公开（可选）
    
    只有文件上传者可以更新文件信息
    """
    try:
        # 使用权限服务检查修改权限
        file = PermissionService.check_file_modification_permission(db, file_id, current_user)
        
        # 更新文件信息
        updated_file = FileService.update_file(db, file_id, file_update, current_user)
        
        # 构建响应 - 使用字典转换确保正确设置download_url
        file_dict = {
            "id": updated_file.id,
            "user_id": updated_file.user_id,
            "filename": updated_file.filename,
            "file_size": updated_file.file_size,
            "file_type": updated_file.file_type,
            "description": updated_file.description,
            "is_public": updated_file.is_public,
            "created_at": updated_file.created_at,
            "updated_at": updated_file.updated_at,
            "download_url": f"/files/{updated_file.id}/download"
        }
        response_data = FileResponse(**file_dict)
        
        return SuccessResponse(
            code=200,
            message="文件信息更新成功",
            data=response_data
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新文件信息失败: {str(e)}"
        )

@files_router.delete("/{file_id}", response_model=SuccessResponse, tags=["文件"])
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除文件
    
    - **file_id**: 文件ID
    
    只有文件上传者可以删除文件
    """
    try:
        # 使用权限服务检查删除权限
        file = PermissionService.check_file_modification_permission(db, file_id, current_user)
        
        # 删除文件
        FileService.delete_file(db, file_id, current_user)
        
        return SuccessResponse(
            code=200,
            message="文件删除成功",
            data={"file_id": file_id}
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除文件失败: {str(e)}"
        )
