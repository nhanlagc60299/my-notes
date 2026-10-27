# Bài test theo chặng

Mỗi khối kết thúc bằng 1 buổi checkpoint: **build lại từ trí nhớ + làm quiz**. Mục đích: kiến thức "nghe/đọc ở đâu đó" phải biến thành thứ tự trả lời được và tự chạy được.

| Khối | Quiz | Pass |
|---|---|---|
| 🧠 Brain | [01-brain](01-brain.md) | ≥ 4/5 A + C xanh |
| 🛠️ Tools & MCP | [02-tools](02-tools.md) | ≥ 4/5 A + C xanh |
| 🗺️ Planning | [03-planning](03-planning.md) | ≥ 4/5 A + C xanh |
| 💾 Memory | [04-memory](04-memory.md) | ≥ 4/5 A + C xanh |
| 🔄 Environment | [05-environment](05-environment.md) | ≥ 4/5 A + C xanh |
| 🛡️ Guardrails | [06-guardrails](06-guardrails.md) | ≥ 4/5 A + C xanh |
| 📊 Observability & Evals | [07-observability-evals](07-observability-evals.md) | ≥ 4/5 A + C xanh |
| 💸 Cost control | [08-cost-control](08-cost-control.md) | ≥ 4/5 A + C xanh |
| **Phần B** | | |
| 📚 RAG nền tảng + đo retrieval | [09-rag-foundations](09-rag-foundations.md) | ≥ 4/5 A + C xanh |
| ✂️ Chunking & context | [10-chunking-context](10-chunking-context.md) | ≥ 4/5 A + C xanh |
| 🔀 Hybrid · fusion · rerank · filter | [11-hybrid-rerank](11-hybrid-rerank.md) | ≥ 4/5 A + C xanh |
| 🔁 Query transform & routing | [12-query-transform](12-query-transform.md) | ≥ 4/5 A + C xanh |
| 🧠 Memory patterns | [13-memory-patterns](13-memory-patterns.md) | ≥ 4/5 A + C xanh |
| ⚡ Cache · async · resilience | [14-cache-async-resilience](14-cache-async-resilience.md) | ≥ 5/7 A + C xanh |

**Cách làm:** 15 phút, không mở tài liệu → tự chấm phần A bằng đáp án ẩn → phần B gửi Claude chấm ("chấm quiz N") → phần C chạy lệnh. Câu sai ghi vào cột *gap* trong [log](../../../learning/ai-agents-40h.md#log) và thành flashcard ôn lại.

> Test ở phần C tham chiếu file sẽ được tạo trong từng buổi. Trước buổi đó, lệnh sẽ báo "file not found", đây là chuyện bình thường.
