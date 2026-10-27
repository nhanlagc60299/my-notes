# 4. 💾 Memory — ngắn hạn, dài hạn, và RAG

> **Một câu:** Short-term = **state của 1 thread** (checkpointer lưu sau mỗi bước); long-term = **dữ liệu sống qua nhiều thread** (store); RAG = **tìm** đúng mẩu tri thức để nhét vào context lúc cần.

## Analogy SRE

| Agent | SRE |
|---|---|
| Checkpointer + `thread_id` | Timeline của **1 incident channel** — đóng incident là hết |
| Store (namespace, key) | **CMDB / wiki team** — sống qua mọi incident |
| RAG (embeddings + similarity) | Tìm "**incident tương tự**" trong postmortem cũ trước khi debug |

## Cốt lõi (đã kiểm chứng)

- LangGraph tách persistence thành 2 hệ: **checkpointer** (lưu state theo thread → short-term, cũng là nền cho HITL và time-travel) và **store** (dữ liệu ứng dụng ngoài graph state → long-term, cross-thread). Docs gợi ý hầu hết app dùng cả hai. — [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- Dev: `InMemorySaver`, `InMemoryStore`; production phải dùng bản bền (DB). `thread_id` nằm trong `config={"configurable": {"thread_id": ...}}`. — [Memory](https://docs.langchain.com/oss/python/langgraph/add-memory)
- Short-term phình to thì phải **trim / delete / summarize messages**: context window là tài nguyên hữu hạn. — Memory § Manage short-term memory
- Embeddings: text → vector, so bằng cosine similarity; độ dài vector tuỳ model (thường 384–1024). — [Ollama Embeddings](https://docs.ollama.com/capabilities/embeddings) (`client.embed(model, input)`)
- ⚠️ OWASP 2026 **LLM09 Vector and Embedding Weaknesses**: RAG cũng là bề mặt tấn công (tài liệu bị đầu độc).

## Trong lab

Buổi 14 thread → 15 store hồ sơ sender → 16 RAG runbook tự viết bằng cosine.

## Ghi chú của tôi

## Câu hỏi còn mở

-
