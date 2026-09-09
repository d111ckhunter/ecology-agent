# -*- coding: utf-8 -*-
"""
LLM client for text-to-SQL (DeepSeek, OpenAI-compatible).

读取 app.core.config 的 LLM_* 配置；无 API key 时抛出 LLMConfigError。
为便于无 key 联调，支持 AGENT_MOCK=1 走内置 MockLLM（不联网）。
"""

import json
import os
import re

from app.core.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, LLM_TEMPERATURE


class LLMError(RuntimeError):
    pass


class LLMConfigError(LLMError):
    pass


def _parse_json_object(text: str) -> dict | None:
    """宽容解析 LLM 输出的 JSON 对象。"""
    text = (text or "").strip()
    if not text:
        return None
    # 直接解析
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass
    # 若被 markdown 代码围栏包裹
    m = re.search(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.S)
    if m:
        try:
            obj = json.loads(m.group(1))
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass
    # 提取第一个 {...}
    start, end = text.find("{"), text.rfind("}")
    if 0 <= start < end:
        try:
            obj = json.loads(text[start:end + 1])
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass
    return None


class DeepSeekLLM:
    """OpenAI 兼容 chat 封装。"""

    def __init__(self):
        if not LLM_API_KEY:
            raise LLMConfigError(
                "未配置 LLM_API_KEY。请在项目根目录 .env 中填写后重试。"
            )
        try:
            from openai import OpenAI
        except ImportError as e:  # pragma: no cover
            raise LLMConfigError("缺少 openai 依赖: pip install openai") from e
        self.client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
        self.model = LLM_MODEL
        self.temperature = LLM_TEMPERATURE

    def chat(self, messages: list[dict], temperature: float | None = None) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature if temperature is None else temperature,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:  # 网络/鉴权等
            raise LLMError("LLM 调用失败: %s" % e) from e

    def chat_stream(self, messages: list[dict], temperature: float | None = None):
        """流式 chat：逐个 delta 产出文本块（token 级打字机）。"""
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature if temperature is None else temperature,
                stream=True,
            )
            for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
        except Exception as e:
            raise LLMError("LLM 流式调用失败: %s" % e) from e

    def chat_json(self, messages: list[dict]) -> dict | None:
        return _parse_json_object(self.chat(messages))


class MockLLM:
    """无 key 联调用。行为约定：
      - chat_json：SQL 生成。数据类问题返回演示 SQL；闲聊/概念类问题
        （含"你好/介绍/解释/是什么"等）返回 {"sql": null}，用于联调自然语言兜底。
      - chat / chat_stream：回答文本（模拟分块流式，便于前端打字机联调）。
    """

    _CHAT_TRIGGERS = ("你好", "介绍", "解释", "是什么", "什么是", "聊聊", "hello", "hi")

    def __init__(self):
        self._first = True

    def _is_chitchat(self, messages: list[dict]) -> bool:
        last_user = next((m.get("content", "") for m in reversed(messages)
                          if m.get("role") == "user"), "")
        return any(t in last_user for t in self._CHAT_TRIGGERS)

    def chat(self, messages: list[dict], temperature: float | None = None) -> str:
        # 兜底/回答阶段整段文本
        return (
            "（AGENT_MOCK 模式演示）这是由 MockLLM 生成的回答："
            "当前为演示模式，数据库查询链路已打通；"
            "填入 .env 的 LLM_API_KEY 后将由 DeepSeek 生成真实、自然的回答。"
            "演示回答支持 **Markdown 加粗**、`行内代码` 等格式。"
        )

    def chat_stream(self, messages: list[dict], temperature: float | None = None):
        text = self.chat(messages)
        # 模拟 token 级分块（每次 4-8 字符）
        i = 0
        step = 6
        while i < len(text):
            yield text[i:i + step]
            i += step

    def chat_json(self, messages: list[dict]) -> dict | None:
        self._first = False
        if self._is_chitchat(messages):
            return {"sql": None, "reason": "问题不涉及库内数据查询，属闲聊/概念类。"}
        return {
            "thinking": "AGENT_MOCK 模式：返回一条演示 SQL。",
            "sql": (
                "SELECT s.station_code, s.station_name, COUNT(d.monitor_code) AS n_records "
                "FROM hydro_data d "
                "JOIN hydro_station s ON d.station_code = s.station_code "
                "GROUP BY s.station_code, s.station_name "
                "ORDER BY n_records DESC LIMIT 5"
            ),
        }


def get_llm(force_mock: bool = False):
    """工厂：AGENT_MOCK=1 或 force_mock 时返回 MockLLM，否则 DeepSeekLLM。"""
    if force_mock or os.getenv("AGENT_MOCK") == "1":
        return MockLLM()
    return DeepSeekLLM()


if __name__ == "__main__":  # 自检：无 key 时应报配置错误；mock 应可用
    try:
        DeepSeekLLM()
        print("DeepSeekLLM ok (key present)")
    except LLMConfigError as e:
        print("DeepSeekLLM expected error:", e)
    m = get_llm(force_mock=True)
    out = m.chat_json([{"role": "user", "content": "列出各测站记录数"}])
    print("MockLLM json keys:", sorted(out.keys()) if out else None)
