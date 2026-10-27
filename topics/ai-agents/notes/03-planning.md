# 3. 🗺️ Planning & Reasoning — chia mục tiêu thành bước

> **Một câu:** Planning = cho model **không gian suy nghĩ** (CoT/thinking), **hành động rồi quan sát** (ReAct), và **tự kiểm rồi sửa** (Reflexion) — còn graph là cách mình *cố định* vòng lặp đó để kiểm soát được.

## Analogy SRE

- **CoT** = viết hypothesis trước khi gõ lệnh trong lúc xử lý sự cố.
- **ReAct** = vòng OODA khi debug: đoán → `kubectl describe` → đọc output → đoán lại.
- **Reflexion** = pre-merge check: chạy test, đỏ thì sửa, tối đa N lần rồi escalate.

## Cốt lõi (đã kiểm chứng)

- **Workflow vs Agent**: workflow = LLM + tool theo *đường code định sẵn*; agent = LLM *tự điều khiển* quy trình và việc dùng tool. Agent = "LLM dùng tool dựa trên phản hồi môi trường, trong một vòng lặp". — Anthropic BEA
- 5 pattern workflow: **Prompt chaining · Routing · Parallelization · Orchestrator-workers · Evaluator-optimizer**. — Anthropic BEA; LangGraph [Workflows & agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) có code cho từng cái.
- **Reflexion ≈ Evaluator-optimizer**: một LLM sinh, một bước khác đánh giá và trả feedback trong vòng lặp.
- LangGraph Graph API: **State** (dữ liệu chung) + **Nodes** (hàm) + **Edges** (thường / có điều kiện). Graph chạy theo *super-step*. — [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- Thinking của Ollama tách trace ra field `thinking`: đọc được để audit, nhưng **tốn token + thời gian**, nên phải đo bằng eval rồi mới quyết bật hay tắt. — [Ollama Thinking](https://docs.ollama.com/capabilities/thinking)

## Trong lab

Buổi 10 đo think on/off → 11 ReAct graph → 12 validate-and-retry.

## Ghi chú của tôi

<!-- think=True có tăng accuracy không? tăng bao nhiêu giây/email? -->

## Câu hỏi còn mở

-
