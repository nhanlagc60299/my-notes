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

## Chống lười (cho người học ngẫu hứng)

Khung này cố ý được làm cho **dễ bắt đầu** hơn là "đủ kỷ luật":

| Cơ chế | Vì sao | Độ mạnh bằng chứng |
|---|---|---|
| Tự nhớ lại (quiz, câu hỏi đầu email, khởi động mỗi buổi) và ôn giãn cách (thẻ cũ quay lại) | Dunlosky et al. 2013 xếp **practice testing** và **distributed practice** là hai kỹ thuật "high utility" duy nhất; đọc lại, gạch chân, tóm tắt là "low utility" | Mạnh (review lớn) |
| Kế hoạch **"nếu… thì…"** (implementation intention) | Meta-analysis Gollwitzer & Sheeran 2006: d ≈ 0,65 cho việc đạt mục tiêu | Mạnh (meta-analysis) |
| **Phiên mini 10–15 phút** vẫn tính giờ | Hạ rào cản bắt đầu; Kaufman: rào cản lớn nhất là cảm xúc ở giờ đầu | Heuristic |
| Bỏ một hôm thì cứ học tiếp, không "làm lại từ đầu" | Lally et al. 2010 (96 người): trung bình ~66 ngày để thành thói quen, dao động 18–254 ngày. ⚠️ Ý "bỏ 1 ngày không làm hỏng" mới thấy ở nguồn thứ cấp, chưa đối chiếu bài gốc | Trung bình |
| Gắn việc học với thứ mình thích (temptation bundling), vd: chỉ uống cà phê ngon khi học | Milkman et al. 2014: hiệu quả ở giai đoạn đầu rồi nhạt dần. ⚠️ chưa đối chiếu bài gốc | Yếu, mẹo phụ |

**Kế hoạch "nếu… thì…" của tôi** (tự điền, càng cụ thể càng tốt):
- Nếu ___ (vd: ăn tối xong mở laptop) thì ___ (vd: gõ `học tiếp` trước khi mở YouTube).
- Nếu chỉ có 10 phút thì làm phiên mini: đọc email flashcard và trả lời phần ① trước khi xem đáp án.

## Hàng đợi chủ đề

| # | Chủ đề | Trạng thái | File |
|---|---|---|---|
| 1 | AI Agents: Phần A (8 mảnh: Brain → Cost control) + Phần B (Retrieval & Memory) — 40h | 🟢 Đang học | [ai-agents-40h.md](ai-agents-40h.md) |
| 2 | Observability — OpenTelemetry (instrument chính agent ở #1) | ⏳ Chờ | — |

## Template cho chủ đề mới

Copy cấu trúc của [ai-agents-40h.md](ai-agents-40h.md): header (target, nhịp, dữ liệu) → tiêu chí pass → bảng deconstruct (tổng 20h) → danh sách cố tình bỏ → bẫy lỗi thời → curriculum theo khối → log → retro.
