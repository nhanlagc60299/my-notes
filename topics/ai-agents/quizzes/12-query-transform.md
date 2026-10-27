# Quiz 12 — 🔁 Query transformation & routing

**Pass:** ≥ 4/5 câu A **và** phần C xanh.

## A. Kiến thức

1. HyDE làm gì, theo đúng định nghĩa trong docs/paper?
2. Ví dụ "Provide the precise and factual answer for…" trong khoá học là HyDE hay kỹ thuật gì?
3. Kể 3 kiểu query transformation mà docs LlamaIndex liệt kê.
4. Khi nào HyDE làm retrieval **tệ đi**?
5. Mỗi bước rewrite/HyDE/router thêm vào pipeline những chi phí và rủi ro gì?

## B. Tình huống

Email dài 20 dòng của bộ phận kế toán mô tả 3 vấn đề khác nhau (VPN, máy in, quyền thư mục). Thiết kế cách biến đổi query để retrieval trúng cả 3.

## C. Thực hành

```bash
pytest -q tests/test_41_rewrite.py tests/test_42_hyde_router.py
```

<details><summary>Đáp án A</summary>

1. LLM viết một **câu trả lời giả định** cho query, rồi **embed câu trả lời đó** để tìm thay cho query gốc (Gao et al., arXiv:2212.10496).
2. Query rewriting.
3. Biến đổi để dễ embed hơn (vd HyDE); single-step decomposition; multi-step decomposition.
4. Khi LLM bịa câu trả lời giả định sai hướng (vd: nhầm thuật ngữ nội bộ), embedding kéo retrieval về tài liệu sai.
5. Thêm lời gọi LLM (độ trễ, token) và thêm một chỗ nội dung email có thể chèn prompt injection.

</details>
