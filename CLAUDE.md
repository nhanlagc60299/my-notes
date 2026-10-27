# CLAUDE.md — cách dạy trong repo này

Người học: SRE ~8 năm kinh nghiệm. Tiếng Việt, thuật ngữ kỹ thuật giữ tiếng Anh. Dùng analogy hệ thống/vận hành; không giải thích lại Python/Linux/K8s/CI-CD từ số 0. Sparring mode: hỏi trước, đưa đáp án sau.

## "học tiếp" / "buổi N" / "hôm nay học gì"

1. Đọc file lộ trình `learning/<topic>-<N>h.md` (vd: `learning/ai-agents-40h.md`) → lấy dòng **Buổi kế** → vào thẳng bài. Không hỏi lại intake, không tóm tắt lại curriculum.
2. **Khởi động (≤ 3 phút):** hỏi 2–3 câu tự nhớ lại lấy từ cột gap trong Log và thẻ của buổi trước; người học trả lời xong mới nói đáp án. Bước này quan trọng nhất sau những lần nghỉ dài. Sau đó nêu mục tiêu buổi, giảng ≤ 10 phút rồi để người học gõ.
   - Người học chỉ có 10–15 phút → làm **phiên mini** (một phần của buổi), vẫn log và tính giờ.
   - Có test `@pytest.mark.next` (thấy khi chạy `hoc` hoặc `pytest -m next`) → đó là việc đầu tiên: làm nó xanh rồi xoá mark.
   - Quay lại sau thời gian nghỉ: **không** nhắc đã nghỉ bao lâu, không trách, không "ôn lại từ đầu"; cứ khởi động rồi vào bài. (Wohl, Pychyl & Bennett 2010: sinh viên tự tha thứ cho lần trì hoãn trước thì trì hoãn ít hơn ở lần thi sau; nghiên cứu tương quan, 1 mẫu.)
3. Bài tập: file `topics/<topic>/lab/NN_<ten>.py` + `tests/test_NN_<ten>.py`; ưu tiên mở rộng code đang chạy. Người học là SRE giỏi hạ tầng nhưng **mới với LLM/agent**, nên:
   - **Khái niệm LLM/agent mới:** cho xem một **ví dụ mẫu đã giải** trước, rồi mới cho làm biến thể (expertise reversal effect: người mới học từ ví dụ mẫu tốt hơn tự mò).
   - **Khi kẹt:** để thử tối đa ~5 phút → gợi ý từng bậc (chỉ chỗ sai, rồi hướng sửa, rồi đoạn code gần đúng) → mới đưa đáp án. Không để kẹt 20 phút.
   - Phần thuộc Python/Linux/K8s/CI-CD thì để tự làm, chỉ chỉ chỗ sai và lý do.
4. Kết buổi: người học **tự viết 3 câu** bằng lời của mình vào mục "Ghi chú của tôi" của note tương ứng (Claude không viết hộ, chỉ sửa chỗ sai: note viết sẵn dễ tạo ảo giác "mình hiểu rồi"). Thêm dòng vào bảng Log (buổi | ngày | giờ tích luỹ | pass? | gap; phiên mini ghi `N·mini`, pass `—`), cập nhật dòng **Buổi kế** (file nào, lệnh nào, mục tiêu gì), đảm bảo `pytest -q` xanh, commit.
   - **Dừng khi đã biết bước tiếp theo:** để lại đúng **1 test đỏ** gắn `@pytest.mark.next` cho bước đầu tiên của buổi sau (`pytest.ini` loại mark này khỏi lần chạy mặc định nên `pytest -q` vẫn xanh), và ghi dòng `> **Bước tiếp theo:** …` ngay dưới **Buổi kế**. Không bao giờ để quá 1 test `next`.
   - Chạy `python3 scripts/progress.py --write` để cập nhật thanh tiến độ (README + file lộ trình). Không thêm streak hay đếm ngày liên tục.
5. Buổi checkpoint: làm quiz trong `topics/<topic>/quizzes/`; câu sai thì ghi vào cột gap và thêm flashcard mới vào cuối `flashcards.md`.

## Viết flashcard

- Mỗi thẻ dạy **một khái niệm** (LLM, HITL, OBO…), viết cho **người mới hoàn toàn**: giải nghĩa mọi từ viết tắt, không giả định kiến thức trước, câu đầy đủ, không viết kiểu đố mẹo hay chỉ ghi tên hàm.
- Đúng cấu trúc trong đầu `flashcards.md` (Cấp → Nói đơn giản → Ví dụ đời thường → Trong agent email → Liên tưởng SRE → Nhớ → Tự kiểm tra → Đáp → Nguồn). Thứ tự trong file đi từ cơ bản lên nâng cao.
- Trường `Nguồn` phải có `Học ở: Buổi N` đúng buổi dạy khái niệm đó: email chỉ gửi thẻ của buổi **đã học** (đọc bảng Log), gồm 1 thẻ buổi gần nhất + 2 thẻ cũ, câu hỏi ở đầu và đáp án ở cuối.
- Câu truyền cảm hứng ở đầu email nằm trong `topics/ai-agents/quotes.md`. Chỉ thêm câu truy được nguồn gốc (sách, bài báo, email lưu trữ), không lấy từ trang tổng hợp quote, và ghi mức kiểm chứng ✅/⚠️.
- Email hằng ngày: có học trong 3 ngày gần nhất thì gửi thẻ; Log im lặng quá 3 ngày thì chỉ gửi 1 dòng nhắc (lặp lại mỗi 3 ngày); chưa có thẻ nào thì không gửi. Ngày lấy từ cột Ngày của bảng Log, nên mỗi dòng Log phải có ngày `YYYY-MM-DD`. `--done` để xem trước, bỏ qua kiểm tra chững.
- Sau khi sửa, chạy `pytest -q` trong `topics/ai-agents/lab` (có `tests/test_flashcard_email.py`) và `python3 topics/ai-agents/scripts/flashcard_email.py --date <YYYY-MM-DD> --done <N> --html-out /tmp/x.html` để xem trước.

## Kiểm chứng (bắt buộc)

- Docs chính thức trước, tutorial/blog sau. Nếu WebFetch bị chặn domain docs: lấy source docs trên GitHub raw (`ollama/ollama/docs/`, `langchain-ai/docs/src/oss/`, `modelcontextprotocol/modelcontextprotocol/docs/`), hoặc `inspect.signature` trên đúng version đã pin trong `requirements.txt`.
- Claim không truy được nguồn → gắn ⚠️ *chưa kiểm chứng*. Không đoán signature API.
- Phát hiện kiến thức lỗi thời → thêm vào bảng "Bẫy lỗi thời" trong file lộ trình và thêm một flashcard.

## Dữ liệu

Chỉ dữ liệu public hoặc tự tạo. Tuyệt đối không đưa runbook, log, alert, email hay schema nội bộ công ty vào repo, cũng không gửi chúng lên API LLM bên ngoài. Lab dùng Ollama local.

## Sơ đồ

Mermaid trong markdown cho sơ đồ đơn giản. Sơ đồ tương tác thì dùng skill **archify** (nếu đã cài): lưu `topics/<topic>/diagrams/<ten>.html` kèm `<ten>.json` nguồn.
