"""
Pytest 配置文件
设置测试环境和通用 fixtures
"""

import pytest
import asyncio
from typing import Generator, Dict, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db, Base
from app.models.user import User
from app.models.note import Note, NoteVersion
from app.utils.auth import get_password_hash


# 测试数据库配置
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# 创建测试数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# 测试数据库会话
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """测试数据库会话 fixture"""
    # 创建表
    Base.metadata.create_all(bind=engine)
    
    # 创建会话
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # 清理表
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """测试客户端 fixture"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    # 覆盖依赖
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # 清理依赖覆盖
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db: Session) -> User:
    """测试用户 fixture"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_superuser(db: Session) -> User:
    """测试超级用户 fixture"""
    user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        is_active=True,
        is_superuser=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_note(db: Session, test_user: User) -> Note:
    """测试笔记 fixture"""
    note = Note(
        title="测试笔记",
        content="# 测试内容\n\n这是一个测试笔记。",
        summary="测试笔记：这是一个测试笔记。",
        tags=["测试", "示例"],
        user_id=test_user.id
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    
    # 创建初始版本
    version = NoteVersion(
        note_id=note.id,
        title=note.title,
        content=note.content,
        summary=note.summary,
        tags=note.tags,
        version_number=1,
        change_description="初始版本"
    )
    db.add(version)
    db.commit()
    
    return note


@pytest.fixture(scope="function")
def auth_headers(test_user: User) -> Dict[str, str]:
    """认证头 fixture"""
    # 这里应该生成真实的 JWT token，简化起见使用模拟值
    return {"Authorization": "Bearer test_token"}


@pytest.fixture(scope="function")
def superuser_auth_headers(test_superuser: User) -> Dict[str, str]:
    """超级用户认证头 fixture"""
    return {"Authorization": "Bearer admin_token"} 