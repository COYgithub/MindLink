#!/usr/bin/env python3
"""
MindLink 数据库初始化脚本

用于首次启动时创建数据库表结构
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.database import init_db, check_db_connection
from app.core.config import get_settings
from app.models import User, Note, NoteVersion
from app.utils.auth import get_password_hash
from app.core.database import get_db
from app.services.user_service import UserService

def create_superuser(db):
    """创建超级用户"""
    
    # 检查是否已存在超级用户
    existing_superuser = db.query(User).filter(User.is_superuser == True).first()
    if existing_superuser:
        print("超级用户已存在，跳过创建")
        return
    
    # 创建超级用户
    superuser_data = {
        "username": "admin",
        "email": "admin@mindlink.com",
        "password": "admin123",
        "is_superuser": True,
        "is_active": True
    }
    
    try:
        # 创建用户
        hashed_password = get_password_hash(superuser_data["password"])
        superuser = User(
            username=superuser_data["username"],
            email=superuser_data["email"],
            hashed_password=hashed_password,
            is_superuser=True,
            is_active=True
        )
        
        db.add(superuser)
        db.commit()
        db.refresh(superuser)
        
        print("超级用户创建成功:")
        print(f"  用户名: {superuser_data['username']}")
        print(f"  邮箱: {superuser_data['email']}")
        print(f"  密码: {superuser_data['password']}")
        print("  请在生产环境中修改默认密码！")
        
    except Exception as e:
        db.rollback()
        print(f"超级用户创建失败: {e}")

def main():
    """主函数"""
    print("MindLink 数据库初始化脚本")
    print("=" * 50)
    
    try:
        # 获取配置
        settings = get_settings()
        print(f"环境: {settings.ENVIRONMENT}")
        print(f"数据库: {settings.DATABASE_URL}")
        
        # 检查数据库连接
        print("检查数据库连接...")
        if not check_db_connection():
            print("❌ 数据库连接失败")
            return False
        
        print("✅ 数据库连接正常")
        
        # 初始化数据库
        print("初始化数据库表...")
        init_db()
        print("✅ 数据库表创建成功")
        
        # 创建超级用户（仅开发环境）
        if settings.ENVIRONMENT == "development":
            print("创建超级用户...")
            from app.core.database import SessionLocal
            db = SessionLocal()
            try:
                create_superuser(db)
            finally:
                db.close()
        
        print("=" * 50)
        print("🎉 数据库初始化完成！")
        print("现在可以启动 MindLink 应用了")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 