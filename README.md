# llm-api-demo

一个使用 Python 调用 OpenRouter LLM API 的命令行聊天示例。

## 脚本功能

`chat_stream.py` 提供了一个简单的终端聊天程序，主要功能包括：

- 使用 `OPENROUTER_API_KEY` 环境变量读取 OpenRouter API Key。
- 通过 OpenAI Python SDK 连接 OpenRouter API。
- 默认使用 `baidu/cobuddy:free` 模型，也可以在启动时输入其他模型 ID。
- 以流式输出的方式显示模型回复，减少等待感。
- 自动保存聊天记录到 `chat_logs/` 目录，文件格式为 `.jsonl`。
- 支持在聊天过程中切换模型、清空上下文和退出程序。
- 默认系统提示词要求模型使用简体中文回答。

## 环境要求

- Python 3.10 或更高版本
- OpenAI Python SDK
- OpenRouter API Key

安装依赖：

```powershell
pip install openai
```

设置环境变量：

```powershell
$env:OPENROUTER_API_KEY="你的 OpenRouter API Key"
```

## 运行方式

```powershell
python chat_stream.py
```

启动后可以直接回车使用默认模型，也可以输入其他 OpenRouter 模型 ID。

## 交互指令

- `exit` / `quit` / `q`：退出聊天，并清空当前上下文。
- `/model`：切换模型，切换后会自动清空上下文。
- `/clear`：手动清空当前上下文。

## 聊天记录

每次启动脚本都会在 `chat_logs/` 目录下创建一个新的聊天记录文件，例如：

```text
chat_logs/chat_20260612_143000.jsonl
```

每一行都是一条 JSON 记录，包含时间、角色、内容和当前模型，方便后续查看或分析。
