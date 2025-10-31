from openai import OpenAI
from dotenv import load_dotenv
from os import getenv

from PIL import ImageGrab
import io
import base64
from web_server import q

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
# 显示在终端中
def take_screenshot_and_ocr(region=None):
    img = ImageGrab.grab(bbox=region) if region else ImageGrab.grab()
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    print(f" imageData: {img_base64[:50]}...")
    result = get_ocr_result(img_base64)
    return result

def code(region=None):
    result = take_screenshot_and_ocr(region)
    gpt_result = get_code_gpt_result(result)
    q.put(gpt_result)

def person(region=None):
    result = take_screenshot_and_ocr(region)
    gpt_result = get_gpt_person_result(result)
    q.put(gpt_result)


def get_code_gpt_result(prompt: str) -> str:
    client = OpenAI(
        base_url=BASE_URL,
        api_key=API_KEY
    )
    response = client.chat.completions.create(
        model="Qwen/Qwen3-Coder-30B-A3B-Instruct",
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

prev_prompt = ""
def get_gpt_person_result(question: str) -> str:
    global prev_prompt
    prompt = "\n---\n1.根据已有答案回答问题，前后一致\t"
    "2.前文答案未涉及随便选择\t"
    "3.直接给出答案，第1个A第二个B，以此类推，不要做任何解释\n---\n"
    client = OpenAI(
        base_url=BASE_URL,
        api_key=API_KEY
    )
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages = [
            {"role": "user", "content": f"{prev_prompt}{prompt}{question}"}
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

    prev_prompt += question + "\t"+ full_response
    return full_response

