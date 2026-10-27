# 8. 💸 Rate Limiting & Cost Control — trần cho vòng lặp

> **Một câu:** Vòng lặp tự sửa không có trần = **infinite loop có hoá đơn**. Phải có trần *số bước*, trần *token/tiền*, và đường thoái lui êm khi chạm trần.

## Analogy SRE

- `recursion_limit` = **circuit breaker / max retries** của HTTP client.
- `RemainingSteps` = **deadline propagation**: biết còn bao nhiêu "ngân sách" để trả kết quả tạm thay vì timeout cứng.
- Token tracking theo user/agent = **chargeback/showback** cho chi phí cloud.

## Cốt lõi (đã kiểm chứng)

- `recursion_limit` = số **super-step** tối đa cho một lần chạy; vượt → `GraphRecursionError`. Truyền ở `config={"recursion_limit": N}` — **cấp ngoài cùng của config, không nằm trong `configurable`**. — [Graph API § Recursion limit](https://docs.langchain.com/oss/python/langgraph/graph-api)
- ⚠️ Mặc định Python = **1000** từ langgraph **1.0.6** (JS = 25). Tutorial cũ ghi 25 là sai với Python hiện tại; 1000 bước là quá cao cho agent phân loại email, nên **phải tự đặt trần**.
- `RemainingSteps` (`from langgraph.managed import RemainingSteps`) đặt trong State → node đọc được số bước còn lại để **chủ động dừng** (proactive) thay vì chờ exception (reactive). Docs khuyên thiết kế điều kiện dừng rõ ràng, coi `GraphRecursionError` chỉ là lưới an toàn.
- Ollama trả `prompt_eval_count` (token input) và `eval_count` (token output) trong mỗi `ChatResponse` → cộng lại theo email/sender. Local thì "chi phí" = thời gian GPU; quy đổi tiền nếu chuyển sang API.
- ⚠️ OWASP 2026 **LLM06 Unbounded Consumption**.

## Trong lab

Buổi 25.

## Ghi chú của tôi

## Câu hỏi còn mở

-
