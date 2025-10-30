import os
import threading
import keyboard
import pyautogui
from PIL import Image
import pystray
from pystray import MenuItem as item
from gpt import *
from web_server import run_server,q
from dotenv import load_dotenv
from os import getenv
load_dotenv()
# ===========================
# 可配置项
# ===========================
ICON_FILE = "./resources/icon.png"
SCREENSHOT_REGION_HOTKEY = getenv("SCREENSHOT_REGION_HOTKEY")
SCREENSHOT_CANCEL_HOTKEY = getenv("SCREENSHOT_CANCEL_HOTKEY")

# ===========================
# 全局变量
# ===========================
first_point = None
lock = threading.Lock()

def on_hotkey():
    """快捷键触发逻辑"""
    global first_point
    with lock:
        if first_point is None:
            first_point = pyautogui.position()
            print(f"📍 已记录第一个坐标：{first_point}")
        else:
            second_point = pyautogui.position()
            print(f"📍 已记录第二个坐标：{second_point}")
            x1 = min(first_point.x, second_point.x)
            y1 = min(first_point.y, second_point.y)
            x2 = max(first_point.x, second_point.x)
            y2 = max(first_point.y, second_point.y)
            region = (x1, y1, x2, y2)
            print(f"🎯 截图区域: {region}")
            threading.Thread(target=take_screenshot_and_ocr, args=(region,), daemon=True).start()
            first_point = None


def on_cancel_hotkey():  # ✅ 新增
    """清空之前的点"""
    global first_point
    with lock:
        first_point = None
        print("🚫 已取消截图选择。")


# ===========================
# 托盘菜单逻辑
# ===========================
def create_tray_icon():
    """创建托盘图标"""
    def on_exit(icon, item):
        icon.stop()
        os._exit(0)

    menu = (item('退出', on_exit),)

    if not os.path.exists(ICON_FILE):
        image = Image.new('RGB', (64, 64), "gray")
    else:
        image = Image.open(ICON_FILE)

    icon = pystray.Icon("ScreenshotUploader", image, "区域截图上传工具", menu)
    return icon



# ===========================
# 主程序入口
# ===========================
def main():
    keyboard.add_hotkey(SCREENSHOT_REGION_HOTKEY, on_hotkey)
    keyboard.add_hotkey(SCREENSHOT_CANCEL_HOTKEY, on_cancel_hotkey)  # ✅ 新增
    print(f"🎯 已注册快捷键 {SCREENSHOT_REGION_HOTKEY} ：按两次选择区域截图上传")
    print(f"🚫 已注册取消快捷键 {SCREENSHOT_CANCEL_HOTKEY} ：清空截图点")
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    icon = create_tray_icon()
    icon.run()


if __name__ == "__main__":
    main()
