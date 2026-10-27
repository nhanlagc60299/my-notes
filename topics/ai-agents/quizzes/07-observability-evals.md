# Quiz 7 — 📊 Observability & Evals

**Pass:** ≥ 4/5 câu A **và** phần C xanh.

## A. Kiến thức

1. `stream_mode` nào của LangGraph phát state update sau mỗi bước, đủ để dựng trace?
2. Một span trong trace agent tối thiểu nên có những field nào?
3. Golden dataset khác gì test unit thường? Nó bảo vệ anh khỏi điều gì khi nâng model?
4. Vì sao trace phải lưu **kết quả tool**, không chỉ output cuối?
5. Eval chạy LLM thật thì chậm và không tất định. Làm sao đưa nó vào `pytest` mà CI vẫn ổn định?

## B. Tình huống

Sau khi đổi `gemma4` sang model khác, accuracy giữ nguyên 83% nhưng 1/3 email injection lọt qua. Gate của anh có bắt được không? Viết lại tiêu chí gate để chắc chắn bắt được.

## C. Thực hành

```bash
pytest -q tests/test_23_trace.py tests/test_eval_gate.py
```

<details><summary>Đáp án A</summary>

1. `stream_mode="updates"`.
2. Node/step, tên tool + arguments, output/kết quả tool, latency, token (input/output), thread/run id.
3. Golden dataset đo **chất lượng hành vi** trên ví dụ thật có nhãn; nó bắt **regression âm thầm** khi đổi prompt/model.
4. Agent ra quyết định dựa trên ground truth từ môi trường mỗi bước; sai thường bắt đầu từ một kết quả tool bị hiểu sai.
5. Tách 2 tầng: CI chạy với **kết quả đã cache/FakeLLM** (tất định); eval với LLM thật chạy định kỳ/thủ công, ghi kết quả vào file để gate đọc.

</details>
