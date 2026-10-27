"""LLM factory — điểm duy nhất code lab chạm vào model.

LLM_BACKEND=fake   (mặc định) → FakeLLM: không cần mạng/Ollama, test chạy offline.
LLM_BACKEND=ollama            → OllamaLLM: gọi Ollama local (http://localhost:11434).

Cả hai trả về đúng kiểu `ollama.ChatResponse`, nên code lab viết một lần,
đổi backend chỉ bằng biến môi trường (giống đổi endpoint qua config, không sửa code).

Verified với ollama-python 0.6.3 (pin trong requirements.txt):
  Client.chat(model, messages, *, tools, stream, think, format, options, keep_alive)
"""
from __future__ import annotations

import os
from typing import Callable, Sequence

from ollama import ChatResponse, Client, Message

DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "gemma4")  # có tool calling trong Ollama (model/parsers/gemma4.go)


class OllamaLLM:
    def __init__(self, model: str = DEFAULT_MODEL, host: str | None = None, think: bool | None = False):
        self.model = model
        self.client = Client(host=host or os.getenv("OLLAMA_HOST", "http://localhost:11434"))
        # think=False: tắt reasoning trace cho nhanh; Buổi 10 sẽ bật lên để so sánh.
        self.think = think

    def chat(self, messages: Sequence[dict | Message], **kwargs) -> ChatResponse:
        kwargs.setdefault("think", self.think)
        return self.client.chat(model=self.model, messages=messages, **kwargs)


class FakeLLM:
    """Model giả để test: trả lời theo script (list) hoặc theo hàm rule(messages, **kwargs) -> str.

    Ghi lại mọi lời gọi vào `.calls` để test assert được "agent đã gửi gì cho model".
    """

    def __init__(self, replies: Sequence[str] | Callable[..., str] | None = None):
        self.replies = replies if replies is not None else keyword_rule
        self.calls: list[dict] = []

    def chat(self, messages: Sequence[dict | Message], **kwargs) -> ChatResponse:
        self.calls.append({"messages": list(messages), **kwargs})
        if callable(self.replies):
            content = self.replies(messages, **kwargs)
        else:
            content = self.replies[min(len(self.calls), len(self.replies)) - 1]
        return ChatResponse(
            model="fake",
            message=Message(role="assistant", content=content),
            prompt_eval_count=sum(len(str(_content(m)).split()) for m in messages),
            eval_count=len(content.split()),
        )


def _content(m: dict | Message) -> str:
    return m["content"] if isinstance(m, dict) else (m.content or "")


def keyword_rule(messages, **_) -> str:
    """'Model' ngây thơ dựa trên từ khoá — baseline để so với LLM thật ở Buổi 3."""
    text = _content(messages[-1]).lower()
    rules = [
        ("phishing", ["verify your password", "account will be suspended", "click here", "gift card"]),
        ("alert", ["[firing", "alertmanager", "severity=", "[resolved"]),
        ("incident", ["outage", "down for", "customers cannot", "sev1", "sev2", "error rate"]),
        ("change_request", ["change request", "cr-", "maintenance window", "approve the deploy"]),
        ("access_request", ["access to", "permission", "grant", "vpn account"]),
        ("vendor", ["invoice", "license", "renewal", "scheduled maintenance"]),
    ]
    for label, words in rules:
        if any(w in text for w in words):
            return label
    return "newsletter"


def get_llm() -> OllamaLLM | FakeLLM:
    backend = os.getenv("LLM_BACKEND", "fake")
    if backend == "ollama":
        return OllamaLLM()
    if backend == "fake":
        return FakeLLM()
    raise ValueError(f"LLM_BACKEND không hợp lệ: {backend!r} (dùng 'fake' hoặc 'ollama')")
