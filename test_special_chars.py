#!/usr/bin/env python3
"""
测试脚本：验证笔记特殊字符处理功能

此脚本创建一个包含特殊字符的测试笔记，验证修改是否生效
"""

import sys
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/notes"
AUTH_TOKEN = "your_auth_token_here"  # 需要替换为实际的认证token

def test_create_note_with_special_chars():
    """测试创建包含特殊字符的笔记"""
    print("测试创建包含特殊字符的笔记...")
    
    # 准备包含各种特殊字符的内容
    test_content = """
# 特殊字符测试

## 中文标点符号
这是中文引号：""、''、《》、【】

## 英文标点符号
!@#$%^&*()_+-=[]{}|;:,.<>?/

## 换行符
这是第一行
这是第二行
这是第三行

## 转义字符
\t\n\r\\

## 混合内容
包含各种"特殊"字符'和[标点]符号的测试内容！
    """
    
    note_data = {
        "title": "特殊字符测试笔记",
        "content": test_content,
        "tags": ["测试", "特殊字符"]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    
    try:
        response = requests.post(
            BASE_URL,
            headers=headers,
            data=json.dumps(note_data, ensure_ascii=False)
        )
        
        if response.status_code == 200:
            print("✅ 创建成功！响应:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            return response.json().get("data", {}).get("id")
        else:
            print(f"❌ 创建失败！状态码: {response.status_code}")
            print("响应:", response.text)
            return None
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return None

def test_update_note_with_special_chars(note_id):
    """测试更新笔记添加更多特殊字符"""
    if not note_id:
        print("跳过更新测试，因为没有有效的笔记ID")
        return
    
    print(f"测试更新笔记 {note_id} 添加更多特殊字符...")
    
    update_content = """
# 更新后的特殊字符测试

## 额外的特殊字符
~`₤€¥$¢©®™§¶|¦

## 多行文本
第一行
第二行
第三行

## 引号嵌套
"这是"嵌套"引号"'
    """
    
    update_data = {
        "content": update_content,
        "change_description": "更新包含特殊字符的内容"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/{note_id}",
            headers=headers,
            data=json.dumps(update_data, ensure_ascii=False)
        )
        
        if response.status_code == 200:
            print("✅ 更新成功！响应:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ 更新失败！状态码: {response.status_code}")
            print("响应:", response.text)
            return False
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return False

def main():
    print("=" * 60)
    print(f"特殊字符处理测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("注意：请确保替换脚本中的 AUTH_TOKEN 为有效的认证token")
    print("测试将验证：")
    print("1. 创建包含特殊字符（中文标点、英文标点、换行符等）的笔记")
    print("2. 更新笔记添加更多特殊字符")
    print("=" * 60)
    
    # 测试创建
    note_id = test_create_note_with_special_chars()
    
    # 测试更新
    test_update_note_with_special_chars(note_id)
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("请检查结果，验证特殊字符是否正确保存")
    print("提示：如果遇到认证问题，请更新脚本中的 AUTH_TOKEN")

if __name__ == "__main__":
    main()
