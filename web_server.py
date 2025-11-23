from bottle import Bottle, template, request, static_file
from gevent.pywsgi import WSGIServer
from dotenv import load_dotenv
from os import getenv
import time
import markdown

load_dotenv()
PORT = int(getenv("PORT"))

app = Bottle()

# 存储所有结果
results = []

# 思考状态管理
is_thinking = False

# 获取当前模型
current_model_index = 0
MODELS = [
    "Qwen/Qwen3-Coder-30B-A3B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "deepseek-ai/DeepSeek-V2-Chat"
]

def get_current_model():
    """获取当前选中的模型"""
    return MODELS[current_model_index]

def set_current_model_index(index):
    """设置当前模型索引"""
    global current_model_index
    current_model_index = index

@app.route('/')
def index():
    """主页"""
    # 获取当前页码，默认为最新结果（最后一页）
    page = request.query.get('page', 'latest')
    if page == 'latest' and results:
        current_index = len(results) - 1
    else:
        try:
            current_index = int(page)
        except:
            current_index = len(results) - 1 if results else 0

    # 确保索引在有效范围内
    if not results:
        current_index = 0
    elif current_index >= len(results):
        current_index = len(results) - 1
    elif current_index < 0:
        current_index = 0

    return template(
        "./resources/template.html",
        results=results,
        current_index=current_index,
        total_count=len(results),
        current_model=get_current_model(),
        is_thinking=is_thinking
    )

@app.route('/static/<filename:path>')
def serve_static(filename):
    """静态文件服务"""
    return static_file(filename, root='./resources/static')

@app.route('/api/thinking/status')
def get_thinking_status():
    """获取思考状态"""
    return {"is_thinking": is_thinking}

@app.route('/api/thinking/start', method='POST')
def start_thinking():
    """开始思考"""
    global is_thinking
    is_thinking = True
    print("🤔 AI开始思考...")
    return {"status": "thinking_started"}

@app.route('/api/thinking/stop', method='POST')
def stop_thinking():
    """停止思考"""
    global is_thinking
    is_thinking = False
    print("✅ AI思考完成")
    return {"status": "thinking_stopped"}

def add_result(result_data):
    """添加新的结果"""
    result_data['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    # 将markdown转换为HTML
    if 'answer' in result_data:
        result_data['answer_html'] = markdown.markdown(result_data['answer'])
    results.append(result_data)
    print(f"✅ 已添加新结果，当前共有 {len(results)} 个结果")

def run_server():
    HOST = '0.0.0.0'
    print(f"服务器即将在 http://{HOST}:{PORT} 启动...")
    server = WSGIServer(
        (HOST, int(PORT)),
        app
    )
    server.serve_forever()