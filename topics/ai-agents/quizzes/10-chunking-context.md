# Quiz 10 — ✂️ Chunking & quản lý context

**Pass:** ≥ 4/5 câu A **và** phần C xanh.

## A. Kiến thức

1. Docs LlamaIndex ghi overlap mặc định là bao nhiêu? Code `SentenceSplitter()` 0.14.25 thật sự dùng bao nhiêu? Bài học là gì?
2. Chunk nhỏ và chunk lớn ảnh hưởng embedding thế nào (theo docs)?
3. `SemanticSplitterNodeParser` quyết định chỗ cắt dựa trên gì? Hai tham số chính và giá trị mặc định?
4. Overlap giải quyết vấn đề gì và gây ra vấn đề gì?
5. Context vượt ngân sách: kể 3 cách xử lý theo thứ tự rẻ → đắt.

## B. Tình huống

Runbook `KubePersistentVolumeFillingUp` dài 146 dòng, có nhiều đoạn lệnh `kubectl`. Đề xuất cấu hình chunk và giải thích bạn sẽ chứng minh lựa chọn đó bằng số đo nào.

## C. Thực hành

```bash
pytest -q tests/test_32_chunk_sweep.py tests/test_34_context_budget.py
```

<details><summary>Đáp án A</summary>

1. Docs: 20. Code: `SentenceSplitter()` → 200 (`Settings.chunk_overlap` cũng 200; 20 chỉ là hằng `DEFAULT_CHUNK_OVERLAP`). Bài học: in ra giá trị thật trên version đã pin.
2. Chunk nhỏ → embedding chính xác hơn; chunk lớn → khái quát hơn nhưng dễ mất chi tiết.
3. Khoảng cách embedding giữa các nhóm câu liền kề; cắt khi vượt percentile. `buffer_size=1`, `breakpoint_percentile_threshold=95`.
4. Giữ ý ở mép chunk; nhưng gây trùng lặp, tốn token trong context.
5. Lọc (cutoff / giảm top-k) → cắt theo token (truncate) → tóm tắt (thêm một lần gọi LLM).

</details>
