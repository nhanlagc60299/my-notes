# Quiz 5 — 🔄 Environment: HITL & Multi-agent

**Pass:** ≥ 4/5 câu A **và** phần C xanh.

## A. Kiến thức

1. Viết 2 dòng code: (a) trong node, dừng để hỏi duyệt; (b) bên ngoài, resume với kết quả "approved".
2. Ba điều kiện để `interrupt()` hoạt động là gì?
3. Vì sao side-effect đặt **trước** `interrupt()` trong cùng node phải idempotent?
4. Đúng hay sai: "`interrupt_before=[...]` lúc compile là cách khuyến nghị để làm HITL."
5. OWASP LLM Top 10 2026 gọi rủi ro "agent có quá nhiều quyền/tự chủ" là gì, mã số mấy?

## B. Tình huống

Router gửi email phishing có injection (e26: "tự cấp cluster-admin…") tới `request_agent` vì nó *trông như* access request. Thiết kế lại để **dù router sai** thì cũng không có quyền nào bị cấp.

## C. Thực hành

```bash
pytest -q tests/test_18_hitl.py tests/test_19_router.py
```

<details><summary>Đáp án A</summary>

1. (a) `decision = interrupt({"action": "create_ticket", "ticket": ticket})` (b) `graph.invoke(Command(resume={"approved": True}), config)`.
2. Có **checkpointer**, có **`thread_id`** trong config, payload **JSON-serializable**.
3. Khi resume, node **chạy lại từ đầu**, nên code trước `interrupt()` sẽ chạy lần nữa.
4. **Sai.** Docs hiện mô tả `interrupt_before/after` là static breakpoint để **debug**; HITL dùng `interrupt()` + `Command(resume=...)`.
5. **LLM03:2026 Excessive Agency.**

</details>
