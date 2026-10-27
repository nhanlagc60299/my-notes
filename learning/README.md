# Learning — phương pháp 20 giờ

Theo Josh Kaufman, *The First 20 Hours* (2013): **deconstruct → learn enough to self-correct → remove barriers → practice ≥ 20 giờ**. Hai nguyên tắc dễ bị quên nhất: *định nghĩa mức "đủ dùng"* và *feedback loop nhanh*.

| Nguyên tắc | Áp dụng ở repo này |
|---|---|
| Một kỹ năng một lúc | Hàng đợi bên dưới. Chủ đề mới chỉ bắt đầu khi chủ đề hiện tại xong. Chủ đề lớn được chia thành nhiều khối 20h nối tiếp (vd: AI Agents = Phần A + Phần B). |
| Target = làm được, không phải "hiểu" | Mỗi lộ trình chốt 1 deliverable + tiêu chí pass đo được. |
| 20% cốt lõi lấy từ docs chính thức | Bảng deconstruct có cột link docs và ngày kiểm chứng. |
| Feedback loop | Mỗi buổi kết thúc bằng `pytest` xanh. Mỗi chặng có một quiz. |
| Remove barriers | Dòng **Buổi kế** ở đầu file lộ trình: bắt đầu được trong 60 giây. |
| Giờ 1–5 là rào cản cảm xúc | Buổi đầu luôn có thứ chạy được trong 15 phút. Code xấu cũng được. |

> Ghi chú khoa học: con số "20 giờ" và "5 giờ đầu" là **heuristic** của Kaufman, không phải kết quả thần kinh học. Những thứ có bằng chứng là *spacing effect* (ôn giãn cách, nên mới có flashcard quay vòng) và *củng cố trí nhớ khi ngủ* (nên học đều tốt hơn học dồn).

## Hàng đợi chủ đề

| # | Chủ đề | Trạng thái | File |
|---|---|---|---|
| 1 | AI Agents: Phần A (8 mảnh: Brain → Cost control) + Phần B (Retrieval & Memory) — 40h | 🟢 Đang học | [ai-agents-40h.md](ai-agents-40h.md) |
| 2 | Observability — OpenTelemetry (instrument chính agent ở #1) | ⏳ Chờ | — |

## Template cho chủ đề mới

Copy cấu trúc của [ai-agents-40h.md](ai-agents-40h.md): header (target, nhịp, dữ liệu) → tiêu chí pass → bảng deconstruct (tổng 20h) → danh sách cố tình bỏ → bẫy lỗi thời → curriculum theo khối → log → retro.
