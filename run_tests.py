#!/usr/bin/env python3
"""
MindLink 测试运行脚本
支持运行不同类型的测试和生成测试报告
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """运行命令并处理结果"""
    print("=" * 60)
    print("正在执行: {}".format(description))
    print("命令: {}".format(" ".join(cmd)))
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 执行成功")
        if result.stdout:
            print("输出:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ 执行失败")
        print("错误代码: {}".format(e.returncode))
        if e.stdout:
            print("标准输出:")
            print(e.stdout)
        if e.stderr:
            print("错误输出:")
            print(e.stderr)
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="MindLink 测试运行器")
    parser.add_argument(
        "--type", 
        choices=["unit", "integration", "all"], 
        default="unit",
        help="测试类型 (默认: unit)"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true",
        help="生成覆盖率报告"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="详细输出"
    )
    parser.add_argument(
        "--markers", 
        action="store_true",
        help="显示所有测试标记"
    )
    
    args = parser.parse_args()
    
    # 检查是否在正确的目录
    if not Path("pytest.ini").exists():
        print("❌ 错误: 请在 MindLink 项目根目录下运行此脚本")
        sys.exit(1)
    
    # 检查测试目录
    if not Path("tests").exists():
        print("❌ 错误: 测试目录不存在")
        sys.exit(1)
    
    # 构建 pytest 命令
    pytest_cmd = ["python", "-m", "pytest"]
    
    # 添加详细输出
    if args.verbose:
        pytest_cmd.extend(["-v", "-s"])
    
    # 添加覆盖率
    if args.coverage:
        pytest_cmd.extend([
            "--cov=app",
            "--cov-report=html",
            "--cov-report=term-missing"
        ])
    
    # 根据测试类型选择测试文件
    if args.type == "unit":
        pytest_cmd.extend(["tests/test_ai_service.py", "tests/test_notes.py"])
        description = "单元测试"
    elif args.type == "integration":
        pytest_cmd.extend(["tests/test_notes.py"])
        description = "集成测试"
    else:  # all
        pytest_cmd.extend(["tests/"])
        description = "所有测试"
    
    # 显示测试标记
    if args.markers:
        print("可用的测试标记:")
        markers_cmd = ["python", "-m", "pytest", "--markers"]
        run_command(markers_cmd, "显示测试标记")
        print()
    
    # 运行测试
    success = run_command(pytest_cmd, description)
    
    if success:
        print("\n🎉 测试执行完成!")
        if args.coverage:
            print("📊 覆盖率报告已生成在 htmlcov/ 目录中")
            print("   打开 htmlcov/index.html 查看详细报告")
    else:
        print("\n💥 测试执行失败!")
        sys.exit(1)


if __name__ == "__main__":
    main() 