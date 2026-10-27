# 🤖 AI Agents

> **Target 40h:** tự build **Email Triage Agent** cho inbox SRE, chạy local bằng Ollama, đủ 8 mảnh ghép (Phần A, 20h), rồi đưa phần Retrieval & Memory lên mức production (Phần B, 20h).
> Lộ trình + log: [learning/ai-agents-40h.md](../../learning/ai-agents-40h.md)

## Bức tranh tổng thể

[![Email Triage Agent — 8 mảnh ghép](diagrams/email-triage-agent.png)](diagrams/email-triage-agent.html)

Sơ đồ tương tác (trace đường đi, zoom, export, dark mode): tải [`diagrams/email-triage-agent.html`](diagrams/email-triage-agent.html) rồi mở bằng trình duyệt. Nguồn: [`email-triage-agent.json`](diagrams/email-triage-agent.json) (Archify v3.2). Muốn sửa thì sửa JSON rồi chạy lại `finalize`.

## 8 mảnh ghép

```mermaid
mindmap
  root((AI Agent))
    Tầng Vận hành
      🧠 Brain
        LLM · structured output
      🛠️ Tools
        tool calling · agent loop · MCP
      🗺️ Planning
        CoT · ReAct · Reflexion
      💾 Memory
        checkpointer · store · RAG
      🔄 Environment
        HITL · multi-agent
    Tầng Hệ thống
      🛡️ Guardrails
        injection shield · output verify
      📊 Observability & Evals
        tracing · golden dataset
      💸 Cost control
        recursion limit · token tracking
```

| # | Mảnh | Note | Quiz | Buổi | Câu hỏi cốt lõi |
|---|---|---|---|---|---|
| 1 | 🧠 Brain | [note](notes/01-brain.md) | [quiz](quizzes/01-brain.md) | 1–4 | LLM chỉ là hàm `messages → message`. Agent đến từ đâu? |
| 2 | 🛠️ Tools | [note](notes/02-tools.md) | [quiz](quizzes/02-tools.md) | 5–9 | Ai thực sự chạy tool? |
| 3 | 🗺️ Planning | [note](notes/03-planning.md) | [quiz](quizzes/03-planning.md) | 10–13 | Khi nào cần agent, khi nào workflow là đủ? |
| 4 | 💾 Memory | [note](notes/04-memory.md) | [quiz](quizzes/04-memory.md) | 14–17 | Thread state, store và RAG khác nhau thế nào? |
| 5 | 🔄 Environment | [note](notes/05-environment.md) | [quiz](quizzes/05-environment.md) | 18–20 | Hành động nào phải dừng chờ người? |
| 6 | 🛡️ Guardrails | [note](notes/06-guardrails.md) | [quiz](quizzes/06-guardrails.md) | 21–22 | Nếu không chặn injection được 100%, bức tường cuối ở đâu? |
| 7 | 📊 Observability & Evals | [note](notes/07-observability-evals.md) | [quiz](quizzes/07-observability-evals.md) | 23–24 | Làm sao biết đổi model không làm agent tệ đi? |
| 8 | 💸 Cost control | [note](notes/08-cost-control.md) | [quiz](quizzes/08-cost-control.md) | 25 | Trần nào chặn vòng lặp tự sửa đốt GPU cả đêm? |

### Phần B — Retrieval & Memory chuyên sâu + resilience (giờ 20 → ~42)

| # | Khối | Note | Quiz | Buổi | Câu hỏi cốt lõi |
|---|---|---|---|---|---|
| 9 | 📚 RAG nền tảng + đo retrieval | [note](notes/09-rag-foundations.md) | [quiz](quizzes/09-rag-foundations.md) | 28–31 | Retrieval tìm đúng bao nhiêu %, đo thế nào? |
| 10 | ✂️ Chunking & context | [note](notes/10-chunking-context.md) | [quiz](quizzes/10-chunking-context.md) | 32–35 | Cỡ chunk nào, chứng minh bằng số nào? |
| 11 | 🔀 Hybrid · fusion · rerank · filter | [note](notes/11-hybrid-rerank.md) | [quiz](quizzes/11-hybrid-rerank.md) | 36–40 | Gộp chữ + nghĩa thế nào, và ai được xem tài liệu nào? |
| 12 | 🔁 Query transform & routing | [note](notes/12-query-transform.md) | [quiz](quizzes/12-query-transform.md) | 41–43 | Viết lại câu hỏi có làm retrieval tốt hơn thật không? |
| 13 | 🧠 Memory patterns | [note](notes/13-memory-patterns.md) | [quiz](quizzes/13-memory-patterns.md) | 44–48 | Nhớ cái gì, ở đâu, và không được nhớ cái gì? |
| 14 | ⚡ Cache · async · resilience | [note](notes/14-cache-async-resilience.md) | [quiz](quizzes/14-cache-async-resilience.md) | 49–54 | Khi model hay retrieval hỏng, agent xuống cấp an toàn thế nào? |

**Tài liệu tham khảo đã kiểm chứng** ([`references/`](references/)): [khoá Retrieval & Memory](references/genai-retrieval-memory-patterns-review.md) · [khoá Reliability/SLO](references/genai-reliability-slo-review.md) · [khoá Model Access & Structured Outputs](references/genai-model-access-structured-outputs-review.md)

## Thư mục

| Path | Nội dung |
|---|---|
| [`notes/`](notes/) | 1 file / mảnh: định nghĩa, analogy SRE, cốt lõi **đã kiểm chứng** (kèm nguồn), ghi chú của tôi |
| [`lab/`](lab/) | Mini-project chạy được: `NN_<ten>.py` + `tests/`, `pytest -q` xanh offline |
| [`quizzes/`](quizzes/) | Bài test cuối mỗi chặng (đáp án ẩn) |
| [`flashcards.md`](flashcards.md) | 81 thẻ khái niệm (Cấp 1 → 7), gửi 3 thẻ/ngày qua Gmail |
| [`references/`](references/) | Báo cáo đối chiếu các khoá học với docs/chuẩn chính thức (đúng / sai / lỗi thời) |
| [`diagrams/`](diagrams/) | Sơ đồ Archify (HTML tương tác + JSON nguồn + PNG preview) |
