"""
MindLink 文件上传功能测试

测试文件上传API的各项功能，包括：
- 文件上传
- 文件下载
- 文件列表获取
- 文件详情获取
- 文件更新
- 文件删除
- 权限控制
"""

import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.models.user import User
from app.models.file import File
from app.schemas.user import UserCreate
from app.utils.auth import create_access_token
from app.services.user_service import UserService

# 创建测试专用的SQLite数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建所有表
Base.metadata.create_all(bind=engine)

# 重写依赖项，使用测试数据库
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 创建测试客户端
client = TestClient(app)


@pytest.fixture
def db():
    """创建数据库会话"""
    # 清理数据库
    db = TestingSessionLocal()
    try:
        # 删除所有文件记录
        db.query(File).delete()
        # 删除所有用户记录
        db.query(User).delete()
        db.commit()
        yield db
    finally:
        # 测试结束后再次清理
        db.query(File).delete()
        db.query(User).delete()
        db.commit()
        db.close()


@pytest.fixture
def test_user(db: Session) -> User:
    """创建测试用户"""
    # 创建测试用户
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword123"
    )
    
    # 使用UserService创建用户
    user = UserService.create_user(db, user_data)
    return user


@pytest.fixture
def test_superuser(db: Session) -> User:
    """创建测试超级用户"""
    # 创建测试超级用户
    user_data = UserCreate(
        username="testsuperuser",
        email="super@example.com",
        password="superpassword123"
    )
    
    # 使用UserService创建用户
    user = UserService.create_user(db, user_data)
    # 设置为超级用户
    user.is_superuser = True
    db.commit()
    return user


@pytest.fixture
def user_token(test_user: User) -> str:
    """创建用户访问令牌"""
    return create_access_token(data={"sub": test_user.username, "user_id": test_user.id})


@pytest.fixture
def superuser_token(test_superuser: User) -> str:
    """创建超级用户访问令牌"""
    return create_access_token(data={"sub": test_superuser.username, "user_id": test_superuser.id})


@pytest.fixture
def test_file():
    """创建测试文件"""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as tmp:
        tmp.write("This is a test file content for MindLink")
        tmp_path = tmp.name
    
    yield tmp_path
    
    # 清理测试文件
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)


def test_upload_file(test_file: str, user_token: str):
    """测试文件上传功能"""
    # 准备文件数据
    with open(test_file, "rb") as f:
        files = {
            "file": ("test_upload.txt", f, "text/plain"),
        }
        data = {
            "description": "Test upload file",
            "is_public": False
        }
        
        # 发送请求
        response = client.post(
            "/files/upload",
            headers={"Authorization": f"Bearer {user_token}"},
            files=files,
            data=data
        )
    
    # 验证响应
    assert response.status_code == 200
    assert response.json()["code"] == 201
    assert response.json()["message"] == "文件上传成功"
    assert "data" in response.json()
    assert "id" in response.json()["data"]
    assert response.json()["data"]["filename"] == "test_upload.txt"
    assert response.json()["data"]["description"] == "Test upload file"
    assert response.json()["data"]["is_public"] == False


def test_get_user_files(test_file: str, user_token: str, db: Session):
    """测试获取用户文件列表"""
    # 先上传一个文件
    with open(test_file, "rb") as f:
        files = {
            "file": ("list_test.txt", f, "text/plain"),
        }
        client.post(
            "/files/upload",
            headers={"Authorization": f"Bearer {user_token}"},
            files=files
        )
    
    # 获取文件列表
    response = client.get(
        "/files/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    # 验证响应
    assert response.status_code == 200
    assert "data" in response.json()
    assert "files" in response.json()["data"]
    assert isinstance(response.json()["data"]["files"], list)
    # 至少有一个文件
    assert len(response.json()["data"]["files"]) >= 1


def test_upload_and_get_file_detail(test_file: str, user_token: str):
    """测试上传文件后获取详情"""
    # 上传文件
    with open(test_file, "rb") as f:
        files = {
            "file": ("detail_test.txt", f, "text/plain"),
        }
        upload_response = client.post(
            "/files/upload",
            headers={"Authorization": f"Bearer {user_token}"},
            files=files
        )
    
    # 获取文件ID
    file_id = upload_response.json()["data"]["id"]
    
    # 获取文件详情
    detail_response = client.get(
        f"/files/{file_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    # 验证响应
    assert detail_response.status_code == 200
    assert detail_response.json()["data"]["id"] == file_id
    assert detail_response.json()["data"]["filename"] == "detail_test.txt"


def test_update_file(test_file: str, user_token: str):
    """测试更新文件信息"""
    # 上传文件
    with open(test_file, "rb") as f:
        files = {
            "file": ("update_test.txt", f, "text/plain"),
        }
        upload_response = client.post(
            "/files/upload",
            headers={"Authorization": f"Bearer {user_token}"},
            files=files
        )
    
    # 获取文件ID
    file_id = upload_response.json()["data"]["id"]
    
    # 更新文件信息
    update_data = {
        "description": "Updated file description",
        "is_public": True
    }
    update_response = client.put(
        f"/files/{file_id}",
        headers={"Authorization": f"Bearer {user_token}"},
        json=update_data
    )
    
    # 验证更新
    assert update_response.status_code == 200
    assert update_response.json()["data"]["description"] == "Updated file description"
    assert update_response.json()["data"]["is_public"] == True


def test_delete_file(test_file: str, user_token: str):
    """测试删除文件"""
    # 上传文件
    with open(test_file, "rb") as f:
        files = {
            "file": ("delete_test.txt", f, "text/plain"),
        }
        upload_response = client.post(
            "/files/upload",
            headers={"Authorization": f"Bearer {user_token}"},
            files=files
        )
    
    # 获取文件ID
    file_id = upload_response.json()["data"]["id"]
    
    # 删除文件
    delete_response = client.delete(
        f"/files/{file_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    # 验证删除
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "文件删除成功"
    
    # 尝试获取已删除的文件，应该返回404
    detail_response = client.get(
        f"/files/{file_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert detail_response.status_code == 404


def test_permission_control(test_file: str, user_token: str, superuser_token: str, db: Session):
    """测试权限控制"""
    # 用户1上传文件
    with open(test_file, "rb") as f:
        files = {
            "file": ("private_test.txt", f, "text/plain"),
        }
        upload_response = client.post(
            "/files/upload",
            headers={"Authorization": f"Bearer {user_token}"},
            files=files,
            data={"is_public": False}
        )
    
    file_id = upload_response.json()["data"]["id"]
    
    # 直接在数据库中创建第二个用户
    user2_data = UserCreate(
        username="testuser2",
        email="test2@example.com",
        password="testpassword123"
    )
    user2 = UserService.create_user(db, user2_data)
    
    # 直接生成token
    user2_token = create_access_token(data={"sub": user2.username, "user_id": user2.id})
    
    # 用户2尝试访问用户1的私有文件，应该被拒绝
    access_response = client.get(
        f"/files/{file_id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert access_response.status_code == 403
    
    # 超级用户可以访问任何文件
    superuser_access = client.get(
        f"/files/{file_id}",
        headers={"Authorization": f"Bearer {superuser_token}"}
    )
    assert superuser_access.status_code == 200


def test_public_file_access(test_file: str, user_token: str):
    """测试公开文件访问"""
    # 上传公开文件
    with open(test_file, "rb") as f:
        files = {
            "file": ("public_test.txt", f, "text/plain"),
        }
        upload_response = client.post(
            "/files/upload",
            headers={"Authorization": f"Bearer {user_token}"},
            files=files,
            data={"is_public": True}
        )
    
    file_id = upload_response.json()["data"]["id"]
    
    # 未认证用户可以访问公开文件
    public_access = client.get(f"/files/{file_id}")
    assert public_access.status_code == 200
    
    # 验证公开文件列表包含该文件
    public_list_response = client.get("/files/public")
    assert public_list_response.status_code == 200
    file_ids = [f["id"] for f in public_list_response.json()["data"]["files"]]
    assert file_id in file_ids

if __name__ == "__main__":
    pytest.main([__file__])
