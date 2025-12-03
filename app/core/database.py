"""
MindLink 数据库配置模块

此模块负责：
- 数据库连接配置
- 数据库会话管理
- 数据库依赖注入
- 支持 MySQL（开发）和 PostgreSQL（生产）
"""

import os
from typing import Generator
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 数据库配置
# 从环境变量读取配置，支持开发和生产环境
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:root@127.0.0.1:3306/mindlink_db?charset=utf8mb4"
)

# 数据库引擎配置
if DATABASE_URL.startswith("sqlit"):
    # SQLite 配置（开发环境）
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,  # 允许多线程访问
        },
        poolclass=StaticPool,            # 使用静态连接池
        echo=os.getenv("SQL_ECHO", "false").lower() == "true"  # 是否显示 SQL 语句
    )
    logger.info("使用 SQLite 数据库（开发环境）")
elif DATABASE_URL.startswith("mysql"):
    # MySQL 配置
    # 建议连接串示例：mysql+pymysql://user:password@host:3306/dbname?charset=utf8mb4
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=os.getenv("SQL_ECHO", "false").lower() == "true"
    )
    logger.info("使用 MySQL 数据库")
else:
    # PostgreSQL 配置（生产环境）
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,              # 连接前检查连接有效性
        pool_recycle=300,                # 连接回收时间（秒）
        echo=os.getenv("SQL_ECHO", "false").lower() == "true"  # 是否显示 SQL 语句
    )
    logger.info("使用 PostgreSQL 数据库")

# 创建数据库会话工厂
# 这是创建数据库会话的标准方式
SessionLocal = sessionmaker(
    autocommit=False,        # 不自动提交事务
    autoflush=False,         # 不自动刷新
    bind=engine              # 绑定到数据库引擎
)

# 创建基础模型类
# 所有数据库模型都将继承这个类
Base = declarative_base()

# 数据库元数据
# 用于管理数据库表结构
metadata = MetaData()

def get_db() -> Generator[Session, None, None]:
    """
    数据库会话依赖注入函数
    
    此函数用于 FastAPI 的依赖注入系统，为每个请求提供数据库会话。
    使用 yield 确保会话在请求结束后正确关闭。
    
    Yields:
        Session: SQLAlchemy 数据库会话对象
        
    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        logger.debug("创建数据库会话")
        yield db
    except Exception as e:
        logger.error(f"数据库会话异常: {str(e)}")
        db.rollback()  # 回滚事务
        raise
    finally:
        logger.debug("关闭数据库会话")
        db.close()

def init_db():
    """
    初始化数据库
    
    创建所有数据库表。通常在应用首次启动时调用。
    """
    try:
        logger.info("开始初始化数据库...")
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库初始化完成")
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise

def close_db():
    """
    关闭数据库连接
    
    清理数据库资源，通常在应用关闭时调用。
    """
    try:
        logger.info("关闭数据库连接...")
        engine.dispose()
        logger.info("数据库连接已关闭")
    except Exception as e:
        logger.error(f"关闭数据库连接失败: {str(e)}")
        raise

# 数据库健康检查
def check_db_connection() -> bool:
    """
    检查数据库连接状态
    
    Returns:
        bool: 连接是否正常
        
    Example:
        if check_db_connection():
            print("数据库连接正常")
        else:
            print("数据库连接异常")
    """
    try:
        with engine.connect() as connection:
            # 执行简单查询测试连接
            connection.execute(text("SELECT 1"))
        logger.debug("数据库连接检查通过")
        return True
    except Exception as e:
        logger.error(f"数据库连接检查失败: {str(e)}")
        return False

# 数据库配置信息
def get_db_info() -> dict:
    """
    获取数据库配置信息
    
    Returns:
        dict: 包含数据库配置信息的字典
    """
        # 推断数据库类型
    if DATABASE_URL.startswith("sqlite"):
        db_type = "sqlite"
    elif DATABASE_URL.startswith("mysql"):
        db_type = "mysql"
    elif DATABASE_URL.startswith("postgres"):
        db_type = "postgresql"
    else:
        db_type = "unknown"
    return {
        "database_url": DATABASE_URL,
        "database_type": db_type,
        "echo": os.getenv("SQL_ECHO", "false").lower() == "true",
        "pool_size": engine.pool.size() if hasattr(engine.pool, 'size') else "N/A",
        "connection_status": "connected" if check_db_connection() else "disconnected"
    } 