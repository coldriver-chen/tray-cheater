#!/usr/bin/env python3
"""
测试思考状态功能
"""
import requests
import time

# 服务器地址
BASE_URL = "http://localhost:80"

def test_thinking_api():
    """测试思考状态API"""
    print("🧪 测试思考状态API...")

    # 测试获取思考状态
    try:
        response = requests.get(f"{BASE_URL}/api/thinking/status")
        print(f"✅ 获取思考状态: {response.json()}")
    except Exception as e:
        print(f"❌ 获取思考状态失败: {e}")
        return

    # 测试开始思考
    try:
        response = requests.post(f"{BASE_URL}/api/thinking/start")
        print(f"✅ 开始思考: {response.json()}")
    except Exception as e:
        print(f"❌ 开始思考失败: {e}")
        return

    # 等待2秒
    print("⏳ 等待2秒...")
    time.sleep(2)

    # 再次获取思考状态
    try:
        response = requests.get(f"{BASE_URL}/api/thinking/status")
        print(f"✅ 当前思考状态: {response.json()}")
    except Exception as e:
        print(f"❌ 获取思考状态失败: {e}")
        return

    # 测试停止思考
    try:
        response = requests.post(f"{BASE_URL}/api/thinking/stop")
        print(f"✅ 停止思考: {response.json()}")
    except Exception as e:
        print(f"❌ 停止思考失败: {e}")
        return

    # 最终获取思考状态
    try:
        response = requests.get(f"{BASE_URL}/api/thinking/status")
        print(f"✅ 最终思考状态: {response.json()}")
    except Exception as e:
        print(f"❌ 获取思考状态失败: {e}")
        return

    print("🎉 思考状态API测试完成！")

if __name__ == "__main__":
    test_thinking_api()