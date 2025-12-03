#!/usr/bin/env python3
"""
MindLink 应用启动脚本

提供便捷的应用启动方式，支持开发和生产环境
"""

import os
import sys
import uvicorn
import argparse
from pathlib import Path

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="MindLink 个人知识管理平台启动脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python run.py                    # 开发模式启动
  python run.py --production      # 生产模式启动
  python run.py --host 0.0.0.0   # 指定主机地址
  python run.py --port 9000       # 指定端口
  python run.py --reload          # 启用热重载
        """
    )
    
    parser.add_argument(
        "--production",
        action="store_true",
        help="生产模式运行"
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="监听主机地址 (默认: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="监听端口 (默认: 8000)"
    )
    
    parser.add_argument(
        "--reload",
        action="store_true",
        help="启用热重载（仅开发模式）"
    )
    
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="工作进程数（仅生产模式）"
    )
    
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="日志级别 (默认: info)"
    )
    
    args = parser.parse_args()
    
    # 设置环境变量
    if args.production:
        os.environ["ENVIRONMENT"] = "production"
        os.environ["DEBUG"] = "false"
        print("🚀 生产模式启动")
    else:
        os.environ["ENVIRONMENT"] = "development"
        os.environ["DEBUG"] = "true"
        print("🔧 开发模式启动")
    
    # 检查环境变量文件
    env_file = Path(".env")
    if env_file.exists():
        print("📝 发现 .env 配置文件")
    else:
        print("⚠️  未发现 .env 配置文件，将使用默认配置")
        print("💡 建议复制 env.example 为 .env 并配置环境变量")
    
    # 检查数据库文件（SQLite）
    if not args.production:
        db_file = Path("mindlink.db")
        if db_file.exists():
            print("💾 发现现有数据库文件")
        else:
            print("🆕 将创建新的 SQLite 数据库文件")
    
    # 启动配置
    config = {
        "app": "app.main:app",
        "host": args.host,
        "port": args.port,
        "log_level": args.log_level,
    }
    
    if args.production:
        # 生产模式配置
        config.update({
            "workers": args.workers,
            "access_log": True,
            "use_colors": False,
        })
        print(f"👥 启动 {args.workers} 个工作进程")
    else:
        # 开发模式配置
        config.update({
            "reload": args.reload or True,  # 开发模式默认启用热重载
            "reload_dirs": ["app"],
            "reload_excludes": ["*.pyc", "*.pyo", "*.pyd"],
        })
        if args.reload:
            print("🔄 热重载已启用")
    
    print(f"🌐 服务地址: http://{args.host}:{args.port}")
    print(f"📚 API 文档: http://{args.host}:{args.port}/docs")
    print(f"❤️  健康检查: http://{args.host}:{args.port}/health")
    print("=" * 50)
    
    try:
        # 启动应用
        uvicorn.run(**config)
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 