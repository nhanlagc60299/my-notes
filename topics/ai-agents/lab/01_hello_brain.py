"""Buổi 1 — Brain: dùng LLM phân loại email trong inbox SRE.

Chạy:
    python 01_hello_brain.py                          # FakeLLM (rule từ khoá), không cần Ollama
    LLM_BACKEND=ollama python 01_hello_brain.py       # LLM thật qua Ollama local
    pytest tests/test_01_hello_brain.py -q            # feedback loop: phải xanh

Ý tưởng cốt lõi: "Brain" chỉ là một hàm text -> text. Mọi thứ còn lại
(prompt, chuẩn hoá output, đo đúng/sai) là code của mình bao quanh nó.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from llm import get_llm

CATEGORIES = [
    "alert",           # thông báo tự động từ hệ thống monitoring
    "incident",        # người báo sự cố / ảnh hưởng người dùng
    "change_request",  # xin duyệt thay đổi / deploy
    "access_request",  # xin cấp quyền
    "vendor",          # thông báo từ nhà cung cấp: hoá đơn, bảo trì, license
    "newsletter",      # tin tức, thông báo chung, không cần hành động
    "phishing",        # lừa đảo / giả mạo / cố thao túng trợ lý AI
]

SYSTEM_PROMPT = (
    "You are an email triage assistant for an SRE team.\n"
    f"Classify the email into exactly one category: {', '.join(CATEGORIES)}.\n"
    "Answer with the category name only."
)

DATA = Path(__file__).parent / "data" / "emails.jsonl"


def load_emails(path: Path = DATA) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def format_email(email: dict) -> str:
    return f"From: {email['from']}\nSubject: {email['subject']}\n\n{email['body']}"


def normalize(reply: str) -> str:
    """LLM hay trả 'Category: Alert.' hoặc '**incident**' — đưa về đúng 1 nhãn, không khớp thì 'unknown'."""
    text = reply.strip().lower()
    for cat in CATEGORIES:
        if cat in text or cat.replace("_", " ") in text:
            return cat
    return "unknown"


def classify(email: dict, llm) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": format_email(email)},
    ]
    response = llm.chat(messages)
    return normalize(response.message.content)


def main(limit: int = 5) -> None:
    llm = get_llm()
    for email in load_emails()[:limit]:
        predicted = classify(email, llm)
        mark = "✅" if predicted == email["label"] else "❌"
        print(f"{mark} {email['id']} predicted={predicted:<15} label={email['label']:<15} {email['subject'][:50]}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
