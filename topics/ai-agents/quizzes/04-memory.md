# Quiz 4 — 💾 Memory

**Pass:** ≥ 4/5 câu A **và** phần C xanh.

## A. Kiến thức

1. Checkpointer và Store khác nhau thế nào (phạm vi + dùng cho gì)?
2. `thread_id` đặt ở đâu trong config? Đổi `thread_id` thì chuyện gì xảy ra?
3. Kể 3 cách docs LangGraph đưa ra để quản lý short-term memory khi messages phình to.
4. Ngoài short-term memory, checkpointer còn là **điều kiện bắt buộc** cho tính năng nào ở khối 5?
5. RAG cũng có rủi ro bảo mật riêng. Tên mục tương ứng trong OWASP LLM Top 10 2026 là gì?

## B. Tình huống

Sender `tuan.do@` hay hỏi về alert đã tự hết. Thiết kế: lưu gì vào Store (namespace, key, value), lúc nào đọc, lúc nào ghi? Dữ liệu nào **không** được lưu (gợi ý: PII)?

## C. Thực hành

```bash
pytest -q tests/test_14_thread_memory.py tests/test_15_store.py tests/test_16_rag.py
```

<details><summary>Đáp án A</summary>

1. Checkpointer: lưu **state theo thread** sau mỗi bước, tức short-term, thread-scoped. Store: dữ liệu ứng dụng **ngoài graph state**, sống qua nhiều thread (long-term).
2. `config={"configurable": {"thread_id": "..."}}`. Đổi `thread_id` = thread mới, state rỗng.
3. **Trim**, **delete**, **summarize** messages.
4. **Human-in-the-loop / `interrupt()`**: phải có checkpointer để lưu state lúc dừng.
5. **LLM09:2026 Vector and Embedding Weaknesses.**

</details>
