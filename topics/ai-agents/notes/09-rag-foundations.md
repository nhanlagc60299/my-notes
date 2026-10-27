# 9. 📚 RAG nền tảng + đo retrieval

> **Một câu:** RAG = tìm đúng mẩu tài liệu rồi đưa vào prompt; chất lượng RAG bị chặn trên bởi chất lượng **retrieval**, nên phải đo retrieval riêng trước khi đo câu trả lời.

## Analogy SRE

RAG giống on-call tra runbook trước khi xử lý: tra sai runbook thì kỹ sư giỏi mấy cũng xử lý sai. Hit rate / MRR là "SLI" của bước tra cứu.

## Cốt lõi (đã kiểm chứng 2026-10-28)

- 5 stage theo LlamaIndex: **Loading → Indexing → Storing → Querying → Evaluation** (`understanding/rag/index.mdx`). ⚠️ Khoá *GenAI Retrieval & Memory Patterns* liệt kê 5 stage khác và **bỏ Evaluation**.
- Quickstart: `SimpleDirectoryReader(dir).load_data()` → `VectorStoreIndex.from_documents(docs)` → `index.as_query_engine().query(...)`. Bản local có sẵn trong docs (`starter_example_local.mdx`, dùng Ollama).
- Tách 2 việc: `index.as_retriever(similarity_top_k=k)` chỉ **tìm**; query engine = retriever + sinh câu trả lời. Đo retrieval thì dùng retriever.
- `RetrieverEvaluator` có các metric: `hit_rate`, `mrr`, `precision`, `recall`, `ap`, `ndcg` (đọc từ `METRIC_REGISTRY`, llama-index-core 0.14.25).
  - **Hit rate@k**: tỉ lệ câu hỏi mà tài liệu đúng nằm trong top-k.
  - **MRR** (Mean Reciprocal Rank): trung bình của 1/(vị trí của tài liệu đúng đầu tiên); đúng ở vị trí 1 → 1.0, vị trí 2 → 0.5.
- ⚠️ Bẫy lỗi thời: `generate_question_context_pairs` (hay thấy trong tutorial) không còn trong `llama_index.core.evaluation` 0.14.25, nên lab tự viết golden set.
- Ollama trong LlamaIndex: `Ollama(model=..., request_timeout=..., context_window=...)`; trường `context_window` mặc định `-1` trong integration 0.11.0, nên **đặt rõ** (liên quan mặc định 4k của Ollama).

## Trong lab

Buổi 28 RAG cơ bản → 29 soi bên trong → 30 `retrieval_golden.jsonl` + hit rate/MRR (baseline Phần B).

## Ghi chú của tôi

## Câu hỏi còn mở

-
