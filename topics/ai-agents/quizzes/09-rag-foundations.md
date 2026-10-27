# Quiz 9 — 📚 RAG nền tảng + đo retrieval

**Pass:** ≥ 4/5 câu A **và** phần C xanh. 15 phút, không mở tài liệu.

## A. Kiến thức

1. Kể 5 stage của RAG theo docs LlamaIndex. Stage nào khoá *GenAI Retrieval & Memory* bỏ sót, và vì sao nó quan trọng?
2. `index.as_retriever()` và `index.as_query_engine()` khác nhau ở đâu? Muốn đo retrieval thì dùng cái nào?
3. Định nghĩa hit rate@3 và MRR. Tài liệu đúng nằm ở vị trí 2 thì reciprocal rank là bao nhiêu?
4. Hàm `generate_question_context_pairs` trong tutorial báo ImportError với `llama-index-core 0.14.25`. Lab xử lý thế nào?
5. Vì sao phải đặt `context_window` rõ ràng khi dùng `Ollama(...)` trong LlamaIndex trên máy < 24 GiB VRAM?

## B. Tình huống

RAG trả lời sai câu "disk /var sắp đầy". Mô tả 3 bước để biết lỗi nằm ở retrieval hay ở bước sinh câu trả lời.

## C. Thực hành

```bash
pytest -q tests/test_28_rag_basic.py tests/test_30_retrieval_eval.py
python 30_retrieval_eval.py      # in hit_rate@3, MRR = baseline Phần B
```

<details><summary>Đáp án A</summary>

1. Loading, Indexing, Storing, Querying, **Evaluation**. Khoá học bỏ Evaluation, trong khi đó là stage duy nhất cho biết tối ưu có hiệu quả không.
2. Retriever chỉ **tìm** node; query engine = retriever + tổng hợp câu trả lời bằng LLM. Đo retrieval thì dùng retriever.
3. Hit rate@3 = tỉ lệ câu hỏi có tài liệu đúng trong top-3. MRR = trung bình 1/(vị trí tài liệu đúng đầu tiên). Vị trí 2 → 0.5.
4. Tự viết golden set (`data/retrieval_golden.jsonl`) gồm câu hỏi và runbook đúng.
5. Ollama mặc định 4k context khi VRAM < 24 GiB; context RAG dễ vượt và bị cắt âm thầm.

</details>
