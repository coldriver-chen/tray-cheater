from bottle import Bottle, template, request, abort
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from queue import Queue
from dotenv import load_dotenv
from os import getenv

load_dotenv()
PORT = int(getenv("PORT"))

app = Bottle()

@app.route('/')
def index():
    """主页"""
    with open("./resources/template.html", "r",encoding="utf-8") as f: content = f.read()
    return template(content)

q = Queue()

# WebSocket 端点
@app.route('/websocket')
def handle_websocket():
    """处理 WebSocket 连接"""
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    
    try:
        while True:
            wsock.send(q.get())
    except WebSocketError:
        print("WebSocket connection closed")

def run_server():
    HOST = '0.0.0.0'
    print(f"服务器即将在 http://{HOST}:{PORT} 启动...")
    print("使用 gevent-websocket 作为 WSGI 服务器后端")
    server = WSGIServer(
        (HOST, int(PORT)),
        app,
        handler_class=WebSocketHandler
    )
    server.serve_forever()