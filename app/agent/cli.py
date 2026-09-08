# -*- coding: utf-8 -*-
"""
CLI for the ecology-agent query agent.

用法（fastapi conda 环境，项目根目录）:
    python -m app.agent.cli                      # 交互式问答
    python -m app.agent.cli --question "..."     # 单发一问
    python -m app.agent.cli --json               # 输出结构化结果(JSON)
    AGENT_MOCK=1 python -m app.agent.cli         # 无 key 演示模式(不联网)
"""

import argparse
import json
import sys

from app.agent.agent import build_agent
from app.agent.llm import LLMConfigError


def ask_once(question: str, as_json: bool = False) -> dict:
    agent = build_agent()
    ans = agent.ask(question)
    d = ans.to_dict()
    if as_json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
    else:
        print("\n【回答】\n%s\n" % d["answer"])
        if d["sql"]:
            print("【SQL】\n%s\n" % d["sql"])
        if d["execution"] and d["execution"]["ok"]:
            ex = d["execution"]
            print("【执行】%d 行 × %d 列，耗时 %.3fs%s" % (
                ex["row_count"], len(ex["columns"]), ex["elapsed"],
                "（结果被截断）" if ex["truncated"] else ""))
        elif d["error"]:
            print("【状态】失败: %s" % d["error"])
    return d


def interactive() -> None:
    print("ecology-agent 问答（输入 exit/quit 退出）")
    print("例: 2024年哪个测站氨氮最高？ / 列出各河段鱼类物种数")
    while True:
        try:
            q = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not q:
            continue
        if q.lower() in ("exit", "quit"):
            break
        try:
            ask_once(q)
        except LLMConfigError as e:
            print("\n[配置错误] %s" % e)
            print("提示: 复制 .env.example 为 .env 并填写 LLM_API_KEY；")
            print("      或使用 AGENT_MOCK=1 python -m app.agent.cli 体验演示模式。")
            break


def main() -> None:
    ap = argparse.ArgumentParser(description="ecology-agent 查询 Agent CLI")
    ap.add_argument("--question", "-q", help="单发提问；缺省进入交互模式")
    ap.add_argument("--json", action="store_true", help="输出结构化 JSON")
    args = ap.parse_args()

    if args.question:
        try:
            ask_once(args.question, as_json=args.json)
        except LLMConfigError as e:
            print("[配置错误] %s" % e)
            sys.exit(2)
    else:
        try:
            interactive()
        except LLMConfigError as e:
            print("[配置错误] %s" % e)
            sys.exit(2)


if __name__ == "__main__":
    main()
