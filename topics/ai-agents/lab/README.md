# Lab — Email Triage Agent (SRE inbox)

Mini-project xuyên suốt 20 giờ. Mỗi buổi = 1 file `NN_<ten>.py` + 1 test `tests/test_NN_<ten>.py`.

## Setup (1 lần, ~10 phút)

```bash
cd topics/ai-agents/lab
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q                      # phải xanh NGAY, không cần Ollama (dùng FakeLLM)

# LLM thật (chạy local, dữ liệu không rời máy):
#   cài Ollama: https://ollama.com/download
ollama pull qwen3              # model dùng trong docs tool-calling chính thức của Ollama
LLM_BACKEND=ollama python 01_hello_brain.py
```

Máy yếu? Đặt `OLLAMA_MODEL=<model nhỏ hơn có hỗ trợ tools>` — kiểm tra tag trên
<https://ollama.com/search?c=tools> trước khi pull (chưa kiểm chứng tag cụ thể từ container học).

## Cấu trúc

| Path | Vai trò |
|---|---|
| `llm.py` | Factory: `LLM_BACKEND=fake` (mặc định, offline) / `ollama`. Cùng trả `ollama.ChatResponse`. |
| `data/emails.jsonl` | 30 email **tự tạo** (golden set) có nhãn `label`, `priority`, `injection`, `pii`. |
| `data/runbooks/` | 6 runbook public từ [prometheus-operator/runbooks](https://github.com/prometheus-operator/runbooks) (Apache-2.0) — dùng cho Tools/RAG. |
| `NN_*.py` | Bài của từng buổi. |
| `tests/` | Feedback loop: `pytest -q` phải xanh trước khi kết buổi. |

## Quy tắc dữ liệu

- Chỉ dữ liệu **public hoặc tự tạo**. Không bao giờ đưa email/log/runbook nội bộ công ty vào đây.
- PII trong dataset (số điện thoại, hộ chiếu) là **giả**, cố tình cài để luyện khối Guardrails.

## Mốc đo

| Mốc | Accuracy trên 30 email |
|---|---|
| Baseline từ khoá (`FakeLLM`) | 19/30 = 63% |
| Target cuối khoá (LLM + prompt + tools) | ≥ 80%, và 3/3 email injection **không** bị thao túng |
