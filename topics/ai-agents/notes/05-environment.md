# 5. 🔄 Environment & Governance — HITL và multi-agent

> **Một câu:** Môi trường là nơi agent nhận **ground truth** sau mỗi hành động. Governance quyết định hành động nào agent **tự làm**, hành động nào phải **dừng chờ người**.

## Analogy SRE

- **HITL** = change approval / `terraform plan` → người đọc → `apply`. Agent được *plan* thoải mái, *apply* phải có chữ ký.
- **Multi-agent** = phân vai trong incident: Incident Commander (router/supervisor), Ops lead, Comms lead. Mỗi vai có quyền và công cụ riêng.

## Cốt lõi (đã kiểm chứng)

- `interrupt(payload)` trong node → LangGraph **lưu state** và trả payload ra ngoài ở field `__interrupt__`; resume bằng `graph.invoke(Command(resume=value), config)` → `value` thành giá trị trả về của `interrupt()`. Cần **checkpointer + thread_id**, payload phải JSON-serializable. — [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- Luật của interrupt: **không** bọc `interrupt` trong try/except; **không** đổi thứ tự các `interrupt` trong node; side-effect **trước** `interrupt` phải **idempotent**, vì node chạy lại từ đầu khi resume. — Interrupts § Rules of interrupts
- `Command(resume=...)` là pattern `Command` **duy nhất** dùng làm input cho `invoke()`; muốn tiếp tục hội thoại thì truyền dict thường. — Graph API
- `interrupt_before/after` lúc compile = **static breakpoint để debug**, không phải cơ chế HITL chính.
- Multi-agent đơn giản nhất = **Routing** (phân loại input → chuyên gia). Orchestrator-workers khi số subtask không biết trước. — Anthropic BEA; LangGraph Workflows § Routing, § Orchestrator-worker
- ⚠️ OWASP 2026 **LLM03 Excessive Agency**: cho agent quá nhiều quyền/tool/tự chủ là rủi ro hàng đầu → HITL + least privilege.

## Trong lab

Buổi 18 duyệt `create_ticket` → 19 router 3 chuyên gia.

## Ghi chú của tôi

## Câu hỏi còn mở

-
