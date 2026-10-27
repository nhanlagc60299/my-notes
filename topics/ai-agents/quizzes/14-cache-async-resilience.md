# Quiz 14 — ⚡ Cache, async, resilience

**Pass:** ≥ 5/7 câu A **và** phần C xanh.

## A. Kiến thức

1. LRU là viết tắt của gì? Khoá *GenAI Retrieval & Memory* nói sai thành gì?
2. Cache key cho retrieval phải gồm những thành phần nào? Thiếu thành phần nào thì lộ dữ liệu?
3. Lỗi nào nên retry, lỗi nào không? Retry cần thêm 2 kỹ thuật gì để không tạo retry storm?
4. Mô tả 3 trạng thái của circuit breaker.
5. Theo SRE Workbook, fast-burn page dùng burn rate và cửa sổ nào? Khoá SLO đặt slow burn thế nào, khác Workbook ra sao?
6. Vì sao không nên để readiness probe của mọi pod phụ thuộc vào một model API dùng chung?
7. Metric token của OpenTelemetry GenAI semconv đang thay đổi thế nào? Cần làm gì khi instrument?

## B. Tình huống

Ollama bị GPU bão hoà, latency P99 từ 2s lên 12s, đồng thời Qdrant trả top-k rỗng cho 30% query. Viết degradation ladder bạn sẽ áp, theo thứ tự, và SLI nào chứng minh đã "về trong ngưỡng".

## C. Thực hành

```bash
pytest -q tests/test_49_cache.py tests/test_51_breaker.py tests/test_52_fallback.py tests/test_53_probes.py
```

<details><summary>Đáp án A</summary>

1. **Least** Recently Used. Khoá học nói "last recently used".
2. Tenant/user + phạm vi quyền + query chuẩn hoá + version index/prompt/model. Thiếu tenant/quyền → người khác quyền nhận chung kết quả.
3. Retry: 429, 500, 502, 503, 504, timeout. Không retry: 400 và lỗi vĩnh viễn. Cần exponential backoff + jitter (và tôn trọng `Retry-After`, giới hạn số lần).
4. CLOSED (chạy bình thường, đếm lỗi) → OPEN (từ chối ngay) → HALF_OPEN (cho vài probe; thành công thì CLOSED, lỗi thì OPEN lại).
5. Workbook: burn rate 14.4, long window 1h + short window 5m (2% budget). Khoá học: slow burn 30m/6h > 2 thì tạo ticket. Workbook: 6h/30m với burn 6 là **page**; ticket là 3d/6h với burn 1 (và 1d/2h với burn 3).
6. Model lỗi thì mọi pod cùng unready, Service không còn endpoint nào → outage toàn bộ do chính probe gây ra.
7. Histogram `gen_ai.client.token.usage` đang được thay bằng `gen_ai.client.inference.usage.*` (tách theo chiều), conventions còn ở trạng thái Development → pin version.

</details>
