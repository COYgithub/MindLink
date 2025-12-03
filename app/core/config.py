"""
MindLink 应用配置模块

此模块负责：
- 环境变量管理
- 应用配置设置
- 安全配置
- 数据库和外部服务配置
"""

import os
from typing import Optional, List
from pydantic import validator
from pydantic_settings  import BaseSettings
import secrets

class Settings(BaseSettings):
    """
    应用配置类
    
    使用 Pydantic 进行配置验证和管理，支持从环境变量读取配置。
    """
    
    # 应用基本信息
    APP_NAME: str = "MindLink"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "个人知识管理平台"
    
    # 环境配置
    ENVIRONMENT: str = "development"  # development, staging, production
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 安全配置
    SECRET_KEY: str = secrets.token_urlsafe(32)  # JWT 签名密钥
    ALGORITHM: str = "HS256"                     # JWT 算法
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30         # 访问令牌过期时间（分钟）
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7           # 刷新令牌过期时间（天）
    
    # 数据库配置
    DATABASE_URL: str = ""
    SQL_ECHO: bool = False
    
    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_DB: int = 0
    
    # OpenAI 配置
    OPENAI_API_KEY: Optional[str] = ""
    OPENAI_BASE_URL: Optional[str] = "https://api.deepseek.com"
    OPENAI_MODEL: str = "deepseek-chat"
    OPENAI_MAX_TOKENS: int = 1000
    
    # CORS 配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    
    # 可信主机配置
    ALLOWED_HOSTS: List[str] = [
        "localhost",
        "127.0.0.1",
        "0.0.0.0"
    ]
    
    # 文件上传配置
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_FILE_EXTENSIONS: str = "txt,md,pdf,doc,docx,xls,xlsx,ppt,pptx,jpg,jpeg,png,gif,bmp,svg,webp,zip,rar,7z,tar,gz,py,js,ts,html,css,json,yaml,xml"
    MAX_FILES_PER_USER: int = 1000  # 每个用户的最大文件数量
    MAX_STORAGE_PER_USER: int = 5 * 1024 * 1024 * 1024  # 每个用户的最大存储容量 (5GB)
    FILE_HASH_ALGORITHM: str = "sha256"  # 文件哈希算法
    ENABLE_FILE_DUPLICATE_CHECK: bool = True  # 是否启用文件重复检查
    
    # 日志配置
    LOG_FILE: Optional[str] = None
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 缓存配置
    CACHE_TTL: int = 3600  # 缓存生存时间（秒）
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """验证环境配置"""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError("环境必须是 development、staging 或 production 之一")
        return v
    
    @validator("DEBUG")
    def validate_debug(cls, v, values):
        """验证调试模式配置"""
        if values.get("ENVIRONMENT") == "production" and v:
            raise ValueError("生产环境不能启用调试模式")
        return v
    
    @validator("CORS_ORIGINS", pre=True)
    def validate_cors_origins(cls, v):
        """验证 CORS 源配置"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ALLOWED_HOSTS", pre=True)
    def validate_allowed_hosts(cls, v):
        """验证可信主机配置"""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    class Config:
        """Pydantic 配置"""
        env_file = ".env"                    # 从 .env 文件读取环境变量
        env_file_encoding = "utf-8"          # 文件编码
        case_sensitive = True                # 区分大小写
        env_prefix = ""                      # 环境变量前缀（空表示无前缀）

# 创建全局配置实例
settings = Settings()

def get_settings() -> Settings:
    """
    获取应用配置实例
    
    Returns:
        Settings: 配置实例
        
    Example:
        config = get_settings()
        print(config.DATABASE_URL)
    """
    return settings

def is_production() -> bool:
    """
    检查是否为生产环境
    
    Returns:
        bool: 是否为生产环境
    """
    return settings.ENVIRONMENT == "production"

def is_development() -> bool:
    """
    检查是否为开发环境
    
    Returns:
        bool: 是否为开发环境
    """
    return settings.ENVIRONMENT == "development"

def is_staging() -> bool:
    """
    检查是否为预发布环境
    
    Returns:
        bool: 是否为预发布环境
    """
    return settings.ENVIRONMENT == "staging"

# 配置验证函数
def validate_config() -> bool:
    """
    验证配置的有效性
    
    Returns:
        bool: 配置是否有效
        
    Raises:
        ValueError: 配置无效时抛出异常
    """
    try:
        # 验证必要的配置项
        if not settings.SECRET_KEY:
            raise ValueError("SECRET_KEY 不能为空")
        
        if not settings.DATABASE_URL:
            raise ValueError("DATABASE_URL 不能为空")
        
        # 验证环境相关配置
        if is_production():
            if settings.DEBUG:
                raise ValueError("生产环境不能启用调试模式")
            
            if not settings.OPENAI_API_KEY:
                raise ValueError("生产环境必须配置 OpenAI API Key")
        
        return True
    except Exception as e:
        raise ValueError("配置验证失败: {}".format(str(e)))

# 配置信息获取函数
def get_config_info() -> dict:
    """
    
    Returns:
        dict: 配置信息字典
    """
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "host": settings.HOST,
        "port": settings.PORT,
        "database_type": "sqlite" if settings.DATABASE_URL.startswith("sqlite") else "postgresql",
        "redis_configured": bool(settings.REDIS_URL),
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "cors_origins_count": len(settings.CORS_ORIGINS),
        "allowed_hosts_count": len(settings.ALLOWED_HOSTS)
    } 