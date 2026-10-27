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
ollama pull gemma4             # hoặc tag Gemma 4 anh đã có; đổi bằng OLLAMA_MODEL=<tag>
LLM_BACKEND=ollama python 01_hello_brain.py
```

**Vì sao Gemma 4** (kiểm chứng 2026-10-28 trên source Ollama): parser `model/parsers/gemma4.go` có `HasToolSupport() = true`; docs Structured Outputs dùng chính `gemma4` làm ví dụ. Thinking tuỳ biến thể (`HasThinkingSupport` theo từng model), nên kiểm ở buổi 10.
Đang có tag khác (vd: `gemma4:e4b`)? Đặt `OLLAMA_MODEL=gemma4:e4b`. ⚠️ Chưa kiểm chứng: danh sách tag/kích thước trên ollama.com (container học bị chặn domain này), nên xem bằng `ollama list` trên máy anh.
Embeddings (buổi 16): docs Ollama dùng `embeddinggemma`.

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
