import os
import json
from datetime import datetime
from openai import OpenAI


DEFAULT_MODEL = "baidu/cobuddy:free"
LOG_DIR = "chat_logs"


def get_client() -> OpenAI:
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError(
            "未检测到 OPENROUTER_API_KEY。请先在 PowerShell 中设置环境变量。"
        )

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "http://localhost",
            "X-OpenRouter-Title": "Python CLI Chat",
        },
    )


def create_log_file() -> str:
    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f"chat_{timestamp}.jsonl")

    return log_file


def save_message(log_file: str, role: str, content: str, model: str | None = None):
    record = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "role": role,
        "content": content,
    }

    if model:
        record["model"] = model

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def stream_chat(client: OpenAI, model: str, messages: list[dict[str, str]]) -> str:
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=1200,
        stream=True,
    )

    full_reply = ""

    for chunk in stream:
        delta = chunk.choices[0].delta.content

        if delta:
            print(delta, end="", flush=True)
            full_reply += delta

    print()
    return full_reply


def main():
    client = get_client()
    log_file = create_log_file()

    model = input(f"请输入模型 ID，直接回车使用默认模型 {DEFAULT_MODEL}：").strip()

    if not model:
        model = DEFAULT_MODEL

    system_prompt = "你必须使用简体中文回答，除非用户明确要求使用其他语言。"

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    save_message(log_file, "system", system_prompt, model)

    print(f"当前模型：{model}")
    print(f"聊天记录将保存到：{log_file}")
    print("输入 exit / quit / q 退出。")
    print("输入 /model 切换模型。")
    print("输入 /clear 手动清空上下文。")
    print("-" * 50)

    while True:
        user_input = input("\n你：").strip()

        if user_input.lower() in {"exit", "quit", "q"}:
            save_message(log_file, "system", "User exited. Context cleared.", model)

            # 退出前清空上下文窗口
            messages.clear()

            print("已退出。上下文已清空。")
            print(f"聊天记录已保存到：{log_file}")
            break

        if user_input == "/model":
            new_model = input("请输入新的模型 ID：").strip()

            if new_model:
                model = new_model

                # 切换模型后也建议清空上下文
                messages = [
                    {
                        "role": "system",
                        "content": system_prompt,
                    }
                ]

                save_message(log_file, "system", f"Model switched to: {model}", model)

                print(f"已切换模型：{model}")
                print("上下文已自动清空。")
            else:
                print("模型未改变。")

            continue

        if user_input == "/clear":
            messages = [
                {
                    "role": "system",
                    "content": system_prompt,
                }
            ]

            save_message(log_file, "system", "Context manually cleared.", model)

            print("上下文已清空。")
            continue

        if not user_input:
            continue

        messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        save_message(log_file, "user", user_input, model)

        print("\nAI：", end="", flush=True)

        try:
            assistant_reply = stream_chat(client, model, messages)

            messages.append(
                {
                    "role": "assistant",
                    "content": assistant_reply,
                }
            )

            save_message(log_file, "assistant", assistant_reply, model)

        except Exception as e:
            error_message = str(e)

            print("\n请求失败：")
            print(error_message)

            save_message(log_file, "error", error_message, model)


if __name__ == "__main__":
    main()