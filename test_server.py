#!/usr/bin/env python3
"""
简单的服务器测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_server import app, add_result

# 添加一些测试数据
def add_test_data():
    test_results = [
        {
            "ocr_text": "这是一个测试问题：什么是Python？",
            "answer": "Python是一种高级编程语言，以其简洁易读的语法而闻名。",
            "model": "Qwen/Qwen3-Coder-30B-A3B-Instruct",
            "timestamp": "2025-01-23 10:00:00"
        },
        {
            "ocr_text": "另一个测试问题：解释一下面向对象编程",
            "answer": "面向对象编程（OOP）是一种编程范式，使用对象和类来组织代码。",
            "model": "Qwen/Qwen2.5-7B-Instruct",
            "timestamp": "2025-01-23 10:05:00"
        }
    ]

    for result in test_results:
        add_result(result)

    print("✅ 已添加测试数据")

if __name__ == "__main__":
    add_test_data()
    print("✅ 服务器测试数据准备完成")
    print("📋 现在可以访问 http://localhost:80 查看结果")