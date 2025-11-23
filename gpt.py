from openai import OpenAI
from dotenv import load_dotenv
from os import getenv

from PIL import ImageGrab
import io
import base64

load_dotenv()

API_KEY = getenv("API_KEY")
BASE_URL = getenv("BASE_URL")
   
def get_ocr_result(base64_image: str) -> str:
    ocr_client = OpenAI(
        api_key=API_KEY, 
        base_url=BASE_URL
    )
    response = ocr_client.chat.completions.create(
        model="deepseek-ai/deepseek-vl2",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/webp;base64,{base64_image}",
                            "detail": "high" 
                        }
                    },
                    {
                        "type": "text",
                        "text": "识别图片中的文字，不要进行翻译。" 
                    }
                ]
            }
        ],stream=True,
    )

    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            text_chunk = chunk.choices[0].delta.content
            print(text_chunk, end='', flush=True)
            full_response += text_chunk
    print("\n\n")

    return full_response

# 截图
# 调用OCR识别
# 调用GPT得到答案
def take_screenshot_and_ocr(region=None):
    img = ImageGrab.grab(bbox=region) if region else ImageGrab.grab()
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    print(f" imageData: {img_base64[:50]}...")
    result = get_ocr_result(img_base64)
    return result


def get_gpt_result(prompt: str, model: str) -> str:
    """使用指定模型获取GPT回答"""
    client = OpenAI(
        base_url=BASE_URL,
        api_key=API_KEY
    )
    response = client.chat.completions.create(
        model=model,
        messages = [
            {"role": "user", "content": f"解答以下这个问题:{prompt}"}
        ],
        stream=True
    )
    full_response = ""
    for chunk in response:
        if not chunk.choices:
            continue
        if content:=chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            full_response += content

    return full_response

