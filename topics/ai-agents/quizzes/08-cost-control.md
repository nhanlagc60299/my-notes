# Quiz 8 — 💸 Cost control

**Pass:** ≥ 4/5 câu A **và** phần C xanh.

## A. Kiến thức

1. `recursion_limit` mặc định của LangGraph **Python** hiện tại là bao nhiêu, từ version nào? Bao nhiêu với bản JS?
2. Code sau sai ở đâu? `graph.invoke(x, {"configurable": {"thread_id": "1", "recursion_limit": 5}})`
3. Vượt `recursion_limit` thì exception gì được raise?
4. `RemainingSteps` dùng để làm gì, khác gì việc bắt exception?
5. OWASP LLM Top 10 2026: mã + tên rủi ro "tiêu thụ tài nguyên không giới hạn"?

## B. Tình huống

Inbox nhận 2.000 email/ngày, trung bình 1.800 token/email, model local 40 token/s output. Ước lượng thời gian GPU/ngày. Ngân sách bước + token nào là hợp lý cho 1 email?

## C. Thực hành

```bash
pytest -q tests/test_25_budget.py
```

<details><summary>Đáp án A</summary>

1. **1000**, từ langgraph **1.0.6**. JS: **25**.
2. `recursion_limit` phải ở **cấp ngoài cùng** của config, không nằm trong `configurable`: `{"recursion_limit": 5, "configurable": {"thread_id": "1"}}`.
3. `GraphRecursionError` (`from langgraph.errors import GraphRecursionError`).
4. Managed value trong State cho node biết **còn bao nhiêu bước** để chủ động dừng/trả kết quả tạm (proactive). Bắt exception là reactive, khi đó graph đã bị cắt.
5. **LLM06:2026 Unbounded Consumption.**

</details>
