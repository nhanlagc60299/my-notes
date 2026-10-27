# 📡 Observability & Reliability — OpenTelemetry cho GenAI

⏳ **Chưa bắt đầu.** Mở sau khi đóng lộ trình [AI Agents](../ai-agents/) (~42 giờ).

Ý tưởng target (chốt lại ở buổi intake): instrument chính **Email Triage Agent** bằng OpenTelemetry, rồi vận hành nó như một dịch vụ production:
- Trace mỗi node/tool call, metric đặt tên theo **OpenTelemetry GenAI semantic conventions**.
- Dashboard SLI theo boundary (retrieval, model, tools) + SLI chất lượng + SLI chi phí.
- SLO + **multiwindow multi-burn-rate alert** theo SRE Workbook; Alertmanager route + inhibit.
- Synthetic deep probe; chaos test nhẹ; postmortem có số liệu.

## Đã kiểm chứng trước (2026-10-28), dùng làm điểm xuất phát

Chi tiết và nguồn: [references/genai-reliability-slo-review.md](../ai-agents/references/genai-reliability-slo-review.md).

| Chủ đề | Chuẩn hiện tại | Bẫy |
|---|---|---|
| OTel GenAI semantic conventions | Repo riêng `open-telemetry/semantic-conventions-genai`, trạng thái **Development** | Repo `semantic-conventions` cũ chỉ còn trang "Moved"; `gen_ai.client.token.usage` đang được thay bằng `gen_ai.client.inference.usage.*`, nên **pin version** |
| Burn-rate alert (SRE Workbook, SLO 30 ngày) | Page: 14.4 @ 1h/5m · 6 @ 6h/30m. Ticket: 3 @ 1d/2h · 1 @ 3d/6h | Một khoá học dùng "slow burn 30m/6h > 2 → ticket", lệch Workbook |
| Alertmanager inhibit | `source_matchers` / `target_matchers` | `source_match` / `target_match` đã deprecated |
| DORA | 5 chỉ số; failed deployment recovery time thay cho MTTR; thêm deployment rework rate | Dashboard chỉ dựa trên MTTR là cách đo cũ |

Kiểm chứng lại docs chính thức tại thời điểm bắt đầu (conventions GenAI đang thay đổi nhanh), không dùng ghi chú cũ làm sự thật.

Cấu trúc sẽ giống `ai-agents/`: `notes/ · lab/ · quizzes/ · flashcards.md · diagrams/`.
