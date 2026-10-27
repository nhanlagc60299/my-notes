# 12. 🔁 Query transformation & routing

> **Một câu:** Câu hỏi người dùng viết thường không giống câu chữ trong tài liệu; biến đổi query (viết lại, tách nhỏ, HyDE) và chọn đúng đường tìm (routing) giúp retrieval trúng hơn, **nếu số đo chứng minh như vậy**.

## Analogy SRE

Như người trực tổng đài dịch lời khách "app không vào được" thành từ khoá kỹ thuật "login 5xx mobile" trước khi tìm trong runbook.

## Cốt lõi (đã kiểm chứng)

- LlamaIndex chia 3 kiểu (*Query transformations*): (1) biến đổi để **dễ embed hơn**, vd HyDE; (2) **single-step decomposition** thành câu hỏi con dễ trả lời; (3) **multi-step decomposition** thành nhiều câu hỏi con.
- **HyDE** (Hypothetical Document Embeddings): LLM viết một **câu trả lời giả định**, rồi **embed câu trả lời đó** để tìm thay cho query gốc. Nguồn: Gao et al., arXiv:2212.10496; `HyDEQueryTransform` + `TransformQueryEngine`.
  - ⚠️ Khoá học minh hoạ bằng ví dụ "Provide the precise and factual answer for…". Đó là **query rewriting**, không phải HyDE.
  - Rủi ro HyDE: câu trả lời giả định sai thì tìm nhầm hướng; tốn thêm một lần gọi LLM. Phải đo.
- `QueryFusionRetriever` với `num_queries > 1` thực chất cũng là một dạng query expansion (LLM sinh các biến thể query).
- **Routing**: chọn retriever hoặc query engine theo loại câu hỏi (LlamaIndex `RouterQueryEngine`). Ở lab: câu có tên alert chính xác → BM25; câu mô tả triệu chứng → vector. Khoá học gọi là "adaptive retrieval"; đó là tên do khoá đặt, không phải API.
- Rewrite/HyDE/router đều là **lời gọi LLM thêm**: cộng độ trễ, token, và là thêm một chỗ có thể bị prompt injection từ nội dung email.

## Trong lab

Buổi 41 rewrite + decomposition → 42 HyDE + router (giữ lại chỉ khi số đo tăng).

## Ghi chú của tôi

## Câu hỏi còn mở

-
