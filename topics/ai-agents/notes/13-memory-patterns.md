# 13. 🧠 Memory patterns: episodic, semantic, procedural

> **Một câu:** Retrieval tìm tri thức **bên ngoài** khi cần; memory giữ những gì agent **đã trải qua và học được** theo thời gian. Production cần cả hai, và memory phải có chính sách ghi rõ ràng.

## Analogy SRE

| Loại | Con người | Agent email | SRE |
|---|---|---|---|
| **Semantic** = facts | Kiến thức học ở trường | Hồ sơ người gửi: "tuan.do@ hay hỏi về alert tự hết" | CMDB: facts về hệ thống |
| **Episodic** = experiences | Việc mình đã làm | Các lần phân loại trước + kết quả, dùng làm ví dụ few-shot | Postmortem các incident cũ |
| **Procedural** = instructions | Kỹ năng đi xe đạp | System prompt + luật phân loại (và code, weights) | Runbook / quy trình chuẩn |

## Cốt lõi (đã kiểm chứng: LangChain docs *Memory concepts*, dựa trên paper CoALA)

- Bảng chính thức: **Semantic → Facts** (vd: facts về user) · **Episodic → Experiences** (vd: hành động trước của agent) · **Procedural → Instructions** (vd: system prompt của agent).
- Semantic memory quản lý theo dạng **profile** (một tài liệu được cập nhật) hoặc **collection** (nhiều mẩu nhỏ). Docs nhắc: **semantic memory ≠ semantic search**.
- Episodic memory thường dùng để agent nhớ **cách** làm xong một việc, hay qua ví dụ few-shot.
- Procedural memory của agent = **model weights + code + prompt**. Agent có thể tự đề xuất sửa prompt của mình (docs có ví dụ node cập nhật instructions).
- Ghi memory: **in the hot path** (ngay lúc trả lời: cập nhật tức thì nhưng thêm độ trễ) hoặc **in the background** (tác vụ nền: không chậm, nhưng memory cập nhật trễ hơn).
- Lưu trữ: LangGraph **store** (namespace + key, có semantic search); dev dùng `InMemoryStore`, production dùng store có DB.
- ⚠️ So với khoá học: khoá xếp "chuẩn coding, tài liệu kỹ thuật" vào semantic memory và "lịch sử hội thoại trong vector DB" vào episodic. Theo docs: lịch sử hội thoại là **short-term memory** (thread/checkpointer); episodic là **kinh nghiệm đã chắt lọc**. Redis (short-term) + Qdrant (long-term) là một lựa chọn thiết kế hợp lý, không phải chuẩn.
- Qdrant chạy **local mode** không cần server: `QdrantClient(":memory:")` hoặc `QdrantClient(path="./qdrant_data")` (`qdrant-client 1.20.0`).
- Rủi ro (khoá học không nói): ghi PII vào memory (LLM02:2026); memory bị đầu độc từ email injection (LLM05, LLM09:2026); procedural memory bị sửa không qua người duyệt (LLM03:2026).

## Trong lab

Buổi 44 map 3 loại → 45 episodic trong Qdrant → 46 chính sách ghi (background, lọc PII, chặn injection) → 47 procedural memory qua HITL.

## Ghi chú của tôi

## Câu hỏi còn mở

-
