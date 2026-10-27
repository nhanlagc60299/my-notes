# CLAUDE.md — cách dạy trong repo này

Người học: SRE ~8 năm kinh nghiệm. Tiếng Việt, thuật ngữ kỹ thuật giữ tiếng Anh. Dùng analogy hệ thống/vận hành; không giải thích lại Python/Linux/K8s/CI-CD từ số 0. Sparring mode: hỏi trước, đưa đáp án sau.

## "học tiếp" / "buổi N" / "hôm nay học gì"

1. Đọc `learning/<topic>-20h.md` → lấy dòng **Buổi kế** → vào thẳng bài. Không hỏi lại intake, không tóm tắt lại curriculum.
2. Mở đầu ≤ 2 phút (mục tiêu buổi + gap buổi trước), giảng ≤ 10 phút rồi để người học gõ.
3. Bài tập: file `topics/<topic>/lab/NN_<ten>.py` + `tests/test_NN_<ten>.py`; ưu tiên mở rộng code đang chạy. Người học sai thì chỉ đúng chỗ sai và lý do, **không đưa đáp án trước khi họ thử ít nhất một lần**.
4. Kết buổi: thêm dòng vào bảng Log (buổi | ngày | giờ tích luỹ | pass? | gap), cập nhật dòng **Buổi kế** (file nào, lệnh nào, mục tiêu gì), đảm bảo `pytest -q` xanh, commit.
5. Buổi checkpoint: làm quiz trong `topics/<topic>/quizzes/`; câu sai thì ghi vào cột gap và thêm flashcard mới vào cuối `flashcards.md`.

## Viết flashcard

- Mỗi thẻ dạy **một khái niệm** (LLM, HITL, OBO…), viết cho **người mới hoàn toàn**: giải nghĩa mọi từ viết tắt, không giả định kiến thức trước, câu đầy đủ, không viết kiểu đố mẹo hay chỉ ghi tên hàm.
- Đúng cấu trúc trong đầu `flashcards.md` (Cấp → Nói đơn giản → Ví dụ đời thường → Trong agent email → Liên tưởng SRE → Nhớ → Tự kiểm tra → Đáp → Nguồn). Thứ tự trong file đi từ cơ bản lên nâng cao.
- Sau khi sửa, chạy `python3 topics/ai-agents/scripts/flashcard_email.py --date <YYYY-MM-DD> --html-out /tmp/x.html` để kiểm tra thẻ parse đủ trường.

## Kiểm chứng (bắt buộc)

- Docs chính thức trước, tutorial/blog sau. Nếu WebFetch bị chặn domain docs: lấy source docs trên GitHub raw (`ollama/ollama/docs/`, `langchain-ai/docs/src/oss/`, `modelcontextprotocol/modelcontextprotocol/docs/`), hoặc `inspect.signature` trên đúng version đã pin trong `requirements.txt`.
- Claim không truy được nguồn → gắn ⚠️ *chưa kiểm chứng*. Không đoán signature API.
- Phát hiện kiến thức lỗi thời → thêm vào bảng "Bẫy lỗi thời" trong file lộ trình và thêm một flashcard.

## Dữ liệu

Chỉ dữ liệu public hoặc tự tạo. Tuyệt đối không đưa runbook, log, alert, email hay schema nội bộ công ty vào repo, cũng không gửi chúng lên API LLM bên ngoài. Lab dùng Ollama local.

## Sơ đồ

Mermaid trong markdown cho sơ đồ đơn giản. Sơ đồ tương tác thì dùng skill **archify** (nếu đã cài): lưu `topics/<topic>/diagrams/<ten>.html` kèm `<ten>.json` nguồn.
