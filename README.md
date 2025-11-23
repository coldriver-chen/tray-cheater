# OCR问答助手

一个基于Python的托盘应用，支持区域截图OCR识别和AI问答功能。

## 功能特点

- 📸 **区域截图**：使用快捷键选择屏幕区域进行截图
- 🔤 **OCR识别**：自动识别图片中的文字
- 🤖 **AI问答**：使用多种AI模型回答问题
- 🔄 **模型切换**：支持快捷键切换不同的AI模型
- 📄 **结果管理**：所有结果保存在列表中，支持翻页查看
- 💻 **简单前端**：基于模板的Web界面，无需WebSocket

## 快捷键配置

在 `.env` 文件中配置快捷键：

```bash
SCREENSHOT_REGION_HOTKEY=ctrl+shift+s    # 截图快捷键
SCREENSHOT_CANCEL_HOTKEY=ctrl+shift+c    # 取消截图
MODEL_SWITCH_HOTKEY=ctrl+shift+m         # 切换模型
```

## 使用方法

1. **启动应用**：
   ```bash
   python main.py
   ```

2. **截图操作**：
   - 按 `Ctrl+Shift+S` 第一次选择截图起点
   - 移动鼠标到终点位置
   - 再次按 `Ctrl+Shift+S` 完成截图
   - 系统会自动进行OCR识别和AI回答

3. **切换模型**：
   - 按 `Ctrl+Shift+M` 循环切换AI模型
   - 当前支持的模型：
     - Qwen/Qwen3-Coder-30B-A3B-Instruct
     - Qwen/Qwen2.5-7B-Instruct
     - deepseek-ai/DeepSeek-V2-Chat

4. **查看结果**：
   - 打开浏览器访问 `http://localhost:80`
   - 使用翻页按钮查看历史结果
   - 每个结果包含OCR文本和AI回答

## 项目结构

```
tray-cheater/
├── main.py              # 主程序，托盘和快捷键管理
├── gpt.py               # OCR和AI问答功能
├── web_server.py        # Web服务器和结果管理
├── resources/
│   └── template.html    # 前端模板
├── .env                 # 配置文件
├── requirements.txt     # 依赖包
└── README.md           # 说明文档
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

在 `.env` 文件中配置：

```bash
API_KEY=your_api_key_here
BASE_URL=https://api.siliconflow.cn/v1
PORT=80
```

## 注意事项

> [!WARNING]
> Special note: Any consequences caused by the use of this software are not the responsibility of the author, and this software is only for learning purposes.