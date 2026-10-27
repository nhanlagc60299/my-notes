# Kiểm chứng: khoá "Reliability, SLOs, and Incident Management for GenAI Systems"

> Tài liệu tham khảo cho **Khối 14 (resilience)** của lộ trình AI Agents và cho chủ đề kế tiếp **Observability & Reliability (OpenTelemetry)**. Không lưu nguyên transcript, chỉ lưu kết quả đối chiếu.
> Kiểm chứng ngày **2026-10-28**. Một số trang gốc (sre.google, dora.dev, grafana.com) bị chặn từ container học, nên mình đối chiếu qua source GitHub chính thức hoặc code của công cụ trích trực tiếp từ nguồn gốc (ghi rõ ở cột nguồn).

**Kết luận nhanh:** Khoá học **vững về nguyên tắc SRE** (đo theo user journey, P95/P99, error budget, timeout + retry có giới hạn + circuit breaker, bulkhead, idempotency key, vai trò incident, postmortem blameless) và có điểm mới đáng giá cho GenAI: **lỗi mềm** (200 OK nhưng sai), **SLI chất lượng** (grounding, retrieval hit), **cost là SLI**, **degradation ladder**. Nhưng cần chỉnh 5 chỗ lệch chuẩn/lỗi thời, và khoá học **chưa có** chuẩn đo lường mới nhất cho GenAI (OpenTelemetry GenAI semantic conventions).

## Bảng đối chiếu

Ký hiệu: ✅ đúng · ⚠️ đúng một phần / cần chỉnh · ❌ sai · 🕐 lỗi thời

| # | Khoá học nói | Kết quả | Chuẩn / nguồn mới nhất |
|---|---|---|---|
| 1 | HTTP 200 có thể che lỗi mềm: trả lời sai, không an toàn, quá chậm; trung bình che giấu P95/P99 | ✅ | Đúng tinh thần SLO theo user journey. Với GenAI phải có SLI chất lượng riêng |
| 2 | 3 nhóm SLI: availability/errors, latency percentile, quality + cost; đo **theo từng boundary** (retrieval, model, tools) | ✅ | Khớp cách chia của OpenTelemetry GenAI semconv: `gen_ai.client.operation.duration`, `gen_ai.execute_tool.duration`, `gen_ai.client.embeddings.duration`… |
| 3 | (Không nhắc) chuẩn đặt tên metric/span cho GenAI | 🕐 **thiếu chuẩn mới** | **OpenTelemetry GenAI semantic conventions** đã **chuyển sang repo riêng** `open-telemetry/semantic-conventions-genai` (repo cũ để lại trang "Moved"). Trạng thái: **Development** (chưa stable, chưa có bản release). Có cả convention cho agent (`gen_ai.invoke_agent.*`), tool, MCP (`mcp.client.operation.duration`) |
| 4 | (Tutorial phổ biến) đo token bằng `gen_ai.client.token.usage` | 🕐 **breaking change** | Changelog (fragment #374, chưa release) **thay** histogram `gen_ai.client.token.usage` bằng các metric tách theo chiều: `gen_ai.client.inference.usage.input_tokens`, `…output_tokens`, `…cache_read.input_tokens`, `…reasoning.output_tokens`… Embeddings tách sang `gen_ai.client.embeddings.duration`. ⚠️ Vì đang Development nên **pin version** convention khi instrument |
| 5 | Fast burn: cửa sổ 5m **và** 1h cùng > **14.4** thì page (theo SRE Workbook) | ✅ | Workbook: 2% budget trong 1h ⇒ burn rate 14.4, short window 5m. Xác nhận qua Sloth `internal/alert/windows/google-30d.yaml`, file ghi rõ lấy số từ Workbook |
| 6 | Slow burn: cửa sổ 30m và 6h > **2** thì tạo ticket | ⚠️ **lệch Workbook** | Workbook: **6h/30m với burn rate 6** (5% budget) là **page**; ticket là **3d/6h với burn rate 1** (10% budget), và 1d/2h (10%). Ngưỡng 2 là tuỳ chỉnh của khoá học |
| 7 | "Burn rate 14 dự báo cạn budget trong **vài giờ**" | ⚠️ | Với SLO 30 ngày, burn 14.4 cạn budget sau 30/14.4 ≈ **50 giờ (~2 ngày)**; ý nghĩa đúng là "tiêu 2% budget trong 1 giờ". (Burn 1000 → cạn trong 43 phút: ✅ đúng phép tính) |
| 8 | Liveness = tiến trình còn sống; Readiness = sẵn sàng nhận traffic; deep probe chạy prompt thật mỗi 1–5 phút, **bỏ qua cache** | ✅ ⚠️ | Đúng với docs Kubernetes (pod không ready thì không nhận traffic qua Service). ⚠️ Khoá học cho readiness flip khi **model chung bị 429**: nếu mọi pod cùng phụ thuộc một model API, tất cả cùng unready ⇒ **tự gây outage toàn bộ**. Nên để deep probe/flag degraded điều khiển hành vi (fallback, tắt tool) thay vì rút pod khỏi Service |
| 9 | Retry chỉ cho lỗi tạm thời: 429, 500, 502, 503, 504, timeout; không retry 400; exponential backoff + **jitter**; giới hạn số lần | ✅ | Thực hành chuẩn. Khoá học **thiếu**: tôn trọng header `Retry-After` (HTTP semantics, RFC 9110) khi nhận 429/503; đặt **retry budget** theo tỉ lệ toàn hệ thống, không chỉ theo request |
| 10 | Circuit breaker: CLOSED → OPEN → HALF_OPEN (probe) → CLOSED; breaker riêng cho từng dependency | ✅ | Pattern chuẩn |
| 11 | Bulkhead: pool riêng cho retrieval / model / tools; chừa capacity cho health probe | ✅ | Pattern chuẩn |
| 12 | Degradation ladder: thu nhỏ context, bỏ tool, đổi model, cache fallback, shed load, giữ critical path | ✅ | Điểm hay nhất của khoá cho GenAI. Bổ sung: mỗi bậc phải **phát cờ `degraded`** vào metric/trace (khoá học có nói) và được **định nghĩa trước** trong runbook |
| 13 | Safe fallback khi `topK_count == 0` hoặc `topK_score < threshold` | ✅ | Khớp trực tiếp Phần B (retrieval eval). Theo dõi `empty_topk_rate`, `low_score_rate`, `safe_fallback_rate` |
| 14 | Cache key gồm prompt template + model version + retrieval context version; TTL ngắn | ✅ ⚠️ | Thiếu **tenant/quyền** trong key (cùng lỗi với khoá Retrieval & Memory) ⇒ lộ dữ liệu chéo |
| 15 | "Degraded = true vẫn tính là success trong availability" | ⚠️ | Là **quyết định định nghĩa SLI**, phải ghi rõ trong SLO doc. Nên có thêm SLI riêng `degraded_rate`, nếu không availability 100% sẽ che việc user nhận câu trả lời kém |
| 16 | Idempotency key cho mỗi hành động ghi (payment, booking…), lưu trạng thái `in_progress/succeeded/failed/expired`, scope theo tool + tenant | ✅ | Khớp FC-36 (idempotency). Header `Idempotency-Key` là **IETF Internet-Draft** (`draft-ietf-httpapi-idempotency-key-header`), chưa phải RFC ⇒ coi là quy ước, kiểm lại trạng thái trước khi trích như chuẩn |
| 17 | Vai trò incident: Incident Commander, Communications, Operations, Subject expert | ⚠️ | Google SRE Book ch.14 *Managing Incidents*: **Incident Command, Operations, Communication, Planning**. Khoá học thiếu vai **Planning** (theo dõi việc dài hạn, bàn giao, ghi lại những gì đã đổi để revert) |
| 18 | Mức severity theo **tác động người dùng**, kể cả hallucination gây hại hoặc output không an toàn | ✅ | Điểm GenAI quan trọng: lỗi chất lượng/an toàn có thể là SEV cao dù uptime xanh |
| 19 | Điều tra theo thứ tự metrics → traces → logs, nối bằng `trace_id` | ✅ | Thực hành chuẩn của OpenTelemetry (context propagation) |
| 20 | Nguyên nhân retrieval tụt: index snapshot lỗi, đổi embedding model làm lệch "hình học vector", ngưỡng/metadata filter siết, đổi prompt template sinh query | ✅ | Rất đúng với Phần B: **đổi embedding model thì phải re-index**; đưa vào checklist change review |
| 21 | Risk score = impact + likelihood + (6 − detectability) | ⚠️ heuristic | Biến thể riêng của khoá. FMEA cổ điển dùng **RPN = Severity × Occurrence × Detection** (nhân). Dùng được nếu team thống nhất; ghi rõ là heuristic |
| 22 | MTTR là thước đo trung tâm của dashboard postmortem | 🕐 | DORA (repo chính thức `dora-team/dora.dev`) đã chuyển từ **MTTR** sang **Failed deployment recovery time**, và có mô hình **5 metric**: change lead time, deployment frequency, failed deployment recovery time (throughput) · change fail rate, **deployment rework rate** (instability). MTTR trung bình dễ gây hiểu lầm vì phân phối lệch: dùng median/percentile và đếm "incident lặp lại" |
| 23 | Postmortem blameless, timeline không ghi tên người; xếp hạng backlog bằng impact + likelihood − effort | ✅ ⚠️ | Blameless ✅. Công thức xếp hạng là heuristic của khoá |
| 24 | Alertmanager: route theo severity, `group_by`, inhibit rule (DependencyDown chặn BurnRateWarning) | ✅ 🕐 | Đúng khái niệm. Lưu ý cú pháp: `source_match`/`target_match` đã **DEPRECATED**, dùng **`source_matchers` / `target_matchers`** (docs `prometheus/alertmanager` `configuration.md`) |
| 25 | "Bỏ qua 429 và cứ gửi thì provider sẽ throttle cả organization" | ⚠️ chưa kiểm chứng | Không tìm thấy trong docs provider; coi là kinh nghiệm cá nhân |
| 26 | Số liệu demo (P99 2.98s, cost tăng $0.0002/request…) | ⚠️ | Số của môi trường stub, không tổng quát |

## Liên hệ với lab (agent email chạy Ollama local)

| Khái niệm khoá học | Áp vào agent email |
|---|---|
| Boundary: retrieval / model / tools | Span + metric riêng cho `lookup_runbook`, Ollama `chat`, Qdrant search; tên theo OTel GenAI semconv (pin version) |
| 429 throttling | Ollama local không có quota như API, nhưng **GPU bão hoà** cho triệu chứng tương tự (latency đuôi, timeout) ⇒ vẫn cần timeout, semaphore, breaker |
| Quality SLI | `empty_topk_rate`, `low_score_rate`, hit_rate trên golden set (offline), tỉ lệ `needs_human` |
| Cost SLI | `prompt_eval_count + eval_count` theo email ⇒ "cost per success" (token / email phân loại đúng) |
| Safe fallback | `category="unknown", needs_human=True` thay vì đoán (đã có ở FC-40, RemainingSteps) |
| Idempotency | `create_ticket` sau HITL: key = (tenant, email_id, action) |

## Nguồn

- OpenTelemetry GenAI semconv: `github.com/open-telemetry/semantic-conventions-genai` (commit `51a0f58`, 2026-10-27): `docs/gen-ai/gen-ai-metrics.md`, `gen-ai-token-metrics.md`, `mcp.md`, `changelog.d/374.breaking.md`, `+embeddings.breaking.md`; trang "Moved" trong `open-telemetry/semantic-conventions/docs/gen-ai/`
- Google SRE Workbook *Alerting on SLOs*, tham số khuyến nghị, xác nhận qua `github.com/slok/sloth/internal/alert/windows/google-30d.yaml`
- Google SRE Book ch.14 *Managing Incidents* (vai trò incident), xác nhận qua kết quả tìm kiếm trỏ tới sre.google
- DORA: `github.com/dora-team/dora.dev` → `hugo/content/guides/dora-metrics/_index.md`
- Alertmanager: `github.com/prometheus/alertmanager/docs/configuration.md` (inhibit rules)
- Kubernetes: `kubernetes/website` → *Configure Liveness, Readiness and Startup Probes*
- IETF: `draft-ietf-httpapi-idempotency-key-header` (Internet-Draft)
