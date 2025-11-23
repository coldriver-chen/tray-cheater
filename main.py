import os
import threading
import keyboard
import pyautogui
from PIL import Image
import pystray
from pystray import MenuItem as item
from gpt import *
from web_server import run_server, add_result
from dotenv import load_dotenv
from os import getenv
load_dotenv()
# ===========================
# 可配置项
# ===========================
ICON_FILE = "./resources/icon.png"
# 截图快捷键
SCREENSHOT_REGION_HOTKEY = getenv("SCREENSHOT_REGION_HOTKEY")
SCREENSHOT_CANCEL_HOTKEY = getenv("SCREENSHOT_CANCEL_HOTKEY")
# 模型切换快捷键
MODEL_SWITCH_HOTKEY = getenv("MODEL_SWITCH_HOTKEY", "ctrl+shift+m")

# ===========================
# 全局变量
# ===========================
first_point = None
lock = threading.Lock()
current_model_index = 0

# 模型列表
MODELS = [
    "Qwen/Qwen3-Coder-30B-A3B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "deepseek-ai/DeepSeek-V2-Chat"
]

def on_screenshot_hotkey():
    global first_point
    with lock:
        if first_point is None:
            first_point = pyautogui.position()
            print(f"📸 已记录第一个坐标：{first_point}")
        else:
            second_point = pyautogui.position()
            print(f"📸 已记录第二个坐标：{second_point}")
            x1 = min(first_point.x, second_point.x)
            y1 = min(first_point.y, second_point.y)
            x2 = max(first_point.x, second_point.x)
            y2 = max(first_point.y, second_point.y)
            region = (x1, y1, x2, y2)
            print(f"🎯 截图区域: {region}")
            threading.Thread(target=process_screenshot, args=(region,), daemon=True).start()
            first_point = None

def on_model_switch_hotkey():
    global current_model_index
    current_model_index = (current_model_index + 1) % len(MODELS)
    current_model = MODELS[current_model_index]
    print(f"🔄 已切换到模型: {current_model}")


def on_cancel_hotkey():
    """清空之前的点"""
    global first_point
    with lock:
        first_point = None
        print("🚫 已取消截图选择。")

def process_screenshot(region=None):
    """处理截图和AI回答"""
    global current_model_index
    try:
        # 截图并OCR识别
        result = take_screenshot_and_ocr(region)
        # 使用当前选择的模型回答问题
        current_model = MODELS[current_model_index]
        gpt_result = get_gpt_result(result, current_model)
        # 添加到结果列表
        add_result({
            "ocr_text": result,
            "answer": gpt_result,
            "model": current_model,
            "timestamp": ""  # 可以添加时间戳
        })
    except Exception as e:
        print(f"❌ 处理截图时出错: {e}")


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
    keyboard.add_hotkey(SCREENSHOT_REGION_HOTKEY, on_screenshot_hotkey)
    keyboard.add_hotkey(MODEL_SWITCH_HOTKEY, on_model_switch_hotkey)
    keyboard.add_hotkey(SCREENSHOT_CANCEL_HOTKEY, on_cancel_hotkey)
    print(f"🎯 已注册截图快捷键 {SCREENSHOT_REGION_HOTKEY} ：按两次选择区域截图")
    print(f"🔄 已注册模型切换快捷键 {MODEL_SWITCH_HOTKEY} ：切换AI模型")
    print(f"🚫 已注册取消快捷键 {SCREENSHOT_CANCEL_HOTKEY} ：清空截图点")
    print(f"📋 当前模型: {MODELS[current_model_index]}")
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    icon = create_tray_icon()
    icon.run()


if __name__ == "__main__":
    main()
