# 1. 🧠 Brain — LLM là "cognitive engine"

> **Một câu:** LLM là một hàm `messages → message`; "trí thông minh" của agent đến từ việc code bao quanh hàm đó cho nó **mục tiêu, ngữ cảnh, schema đầu ra và phản hồi từ môi trường**.

## Analogy SRE

LLM giống một **on-call engineer giỏi nhưng mất trí nhớ sau mỗi cuộc gọi**: mỗi request phải đưa đủ context (system prompt = runbook chung, user message = alert cụ thể). Output không có schema thì như ticket viết tay — không parse được, không tự động hoá được.

## Cốt lõi (đã kiểm chứng)

- `chat(model, messages, *, tools, think, format, options, ...)` → `ChatResponse` với `message.content`, `message.tool_calls`, `message.thinking`, `prompt_eval_count`, `eval_count` — *ollama-python 0.6.3, kiểm bằng `inspect.signature`*.
- **Structured outputs**: truyền JSON schema vào `format` (Pydantic: `Model.model_json_schema()`), validate bằng `Model.model_validate_json(...)`. Docs khuyên **đưa schema vào cả prompt** để model bám tốt hơn. Ollama *cloud* chưa hỗ trợ structured outputs. — [Ollama Structured Outputs](https://docs.ollama.com/capabilities/structured-outputs)
- **Thinking**: model hỗ trợ sẽ trả trace riêng ở field `thinking`, tách khỏi câu trả lời. — [Ollama Thinking](https://docs.ollama.com/capabilities/thinking)
- "Bắt đầu bằng prompt đơn giản, tối ưu bằng evaluation toàn diện; chỉ thêm agent nhiều bước khi giải pháp đơn giản không đủ." — [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

## Trong lab

Buổi 1 `01_hello_brain.py` (classify) → Buổi 2 structured output → Buổi 3 `eval.py` (accuracy).

## Ghi chú của tôi

<!-- Điền khi học: điều gì làm mình bất ngờ, prompt nào chạy tốt/tệ, số liệu accuracy -->

## Câu hỏi còn mở

-
