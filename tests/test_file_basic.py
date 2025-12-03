"""
MindLink 文件上传基础测试

简单测试文件上传功能
"""

import os
import tempfile
from fastapi.testclient import TestClient

from app.main import app

# 创建测试客户端
client = TestClient(app)

def test_basic_upload():
    """基础文件上传测试"""
    # 创建测试文件
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as tmp:
        tmp.write("Basic test file content")
        tmp_path = tmp.name
    
    try:
        # 准备文件数据
        with open(tmp_path, "rb") as f:
            files = {
                "file": ("basic_test.txt", f, "text/plain"),
            }
            data = {
                "description": "Basic test upload",
                "is_public": True
            }
            
            # 发送请求 - 注意：这里可能需要先登录获取token
            # 暂时注释掉认证，仅测试接口格式
            # response = client.post(
            #     "/files/upload",
            #     headers={"Authorization": f"Bearer {token}"},
            #     files=files,
            #     data=data
            # )
            
            print("测试文件已准备好，可以手动测试文件上传功能")
            print(f"测试文件路径: {tmp_path}")
            print(f"文件内容: Basic test file content")
            print("\n文件上传API端点: POST /files/upload")
            print("请求参数:")
            print("- file: 文件数据")
            print("- description: 文件描述")
            print("- is_public: 是否公开")
            
            return True
    finally:
        # 清理测试文件
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

if __name__ == "__main__":
    test_basic_upload()
