# Quiz 1 — 🧠 Brain

**Pass:** ≥ 4/5 câu A **và** phần C xanh. Làm không nhìn tài liệu, 15 phút. Phần B: viết câu trả lời rồi gửi Claude chấm.

## A. Kiến thức

1. Trong Ollama Python, để ép output theo Pydantic model `Triage`, truyền gì vào tham số nào? Validate bằng hàm gì?
2. Docs Ollama khuyên làm thêm gì ngoài việc truyền schema vào `format` để model bám schema tốt hơn?
3. `ChatResponse` có 2 field nào cho biết số token input/output?
4. Đúng hay sai: "Structured outputs hoạt động giống nhau trên Ollama local và Ollama cloud."
5. Theo *Building effective agents*, nên bắt đầu một hệ LLM như thế nào trước khi nghĩ tới agent nhiều bước?

## B. Tình huống

Team anh muốn "dùng LLM tự động phân loại 100% email trong inbox SRE từ tuần sau". Anh sẽ đặt **điều kiện gì** (đo được) trước khi đồng ý bật, và tại sao baseline từ khoá 63% lại quan trọng?

## C. Thực hành

```bash
cd topics/ai-agents/lab && pytest -q tests/test_01_hello_brain.py tests/test_02_structured.py
python eval.py   # in accuracy trên 30 email
```

<details><summary>Đáp án A</summary>

1. `format=Triage.model_json_schema()`; validate bằng `Triage.model_validate_json(response.message.content)`.
2. Đưa JSON schema **dạng chuỗi vào prompt** để "ground" câu trả lời.
3. `prompt_eval_count` (input), `eval_count` (output).
4. **Sai.** Docs ghi: Ollama cloud hiện chưa hỗ trợ structured outputs.
5. Bắt đầu với prompt đơn giản, tối ưu bằng evaluation toàn diện; chỉ thêm hệ agentic nhiều bước khi giải pháp đơn giản không đủ.

</details>
