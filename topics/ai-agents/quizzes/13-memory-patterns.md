# Quiz 13 — 🧠 Memory patterns

**Pass:** ≥ 4/5 câu A **và** phần C xanh.

## A. Kiến thức

1. Theo docs LangChain, semantic / episodic / procedural memory lưu loại thông tin gì? Cho mỗi loại một ví dụ trong agent email.
2. "Semantic memory" và "semantic search" khác nhau thế nào?
3. Procedural memory của agent gồm những thành phần nào?
4. Ghi memory "in the hot path" và "in the background" đánh đổi gì?
5. Kể 3 rủi ro bảo mật khi agent tự ghi memory, kèm mã OWASP 2026.

## B. Tình huống

Khoá học xếp "lịch sử hội thoại trong vector DB" vào episodic memory. Theo docs, lịch sử hội thoại là loại memory nào, và episodic memory đúng nghĩa nên chứa gì?

## C. Thực hành

```bash
pytest -q tests/test_45_episodic_qdrant.py tests/test_46_memory_policy.py tests/test_47_procedural_hitl.py
```

<details><summary>Đáp án A</summary>

1. Semantic = **facts** (hồ sơ người gửi); episodic = **experiences** (các lần xử lý trước, dùng làm few-shot); procedural = **instructions** (system prompt + luật phân loại).
2. Semantic memory là thuật ngữ tâm lý học: lưu facts. Semantic search là kỹ thuật tìm theo nghĩa bằng embedding.
3. Model weights + code của agent + prompt.
4. Hot path: cập nhật ngay nhưng thêm độ trễ trả lời. Background: không làm chậm, nhưng memory cập nhật trễ.
5. Ghi PII (LLM02); memory bị đầu độc từ email injection (LLM05 Data and Model Poisoning, LLM09); agent tự sửa luật không qua người duyệt (LLM03 Excessive Agency).

</details>
