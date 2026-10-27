# Quiz 11 — 🔀 Hybrid, fusion, rerank, filter

**Pass:** ≥ 4/5 câu A **và** phần C xanh.

## A. Kiến thức

1. Viết công thức RRF. LlamaIndex dùng k bằng bao nhiêu và lấy từ đâu?
2. Khoá học nói "re-ranking using Reciprocal Rank Fusion". Sai ở đâu?
3. `QueryFusionRetriever` mặc định `num_queries` bằng bao nhiêu và hệ quả là gì? Muốn hybrid thuần thì đặt sao?
4. `SimilarityPostprocessor(similarity_cutoff=...)` và `SentenceTransformerRerank` khác nhau thế nào?
5. Vì sao metadata filter theo quyền **không** phải bước tuỳ chọn trong hệ nhiều tenant? Liên quan mục OWASP 2026 nào?

## B. Tình huống

Câu hỏi "KubePodCrashLooping payments-api" và câu "app cứ chết rồi tự bật lại". Dự đoán BM25 và vector thắng ở câu nào, và vì sao hybrid + RRF xử lý được cả hai.

## C. Thực hành

```bash
pytest -q tests/test_37_rrf.py tests/test_39_metadata_filter.py
```

<details><summary>Đáp án A</summary>

1. `score(d) = Σ 1/(k + rank_i(d))`; k = 60, theo bài gốc Cormack et al. (SIGIR 2009), có ghi trong source `QueryFusionRetriever`.
2. RRF là **fusion** (gộp danh sách theo thứ hạng), không dùng model để chấm lại; rerank thật dùng cross-encoder hoặc LLM.
3. `num_queries=4`: LLM sinh thêm 3 query (tốn thêm lời gọi LLM). Hybrid thuần: `num_queries=1`.
4. Cutoff **lọc** node điểm thấp; reranker **chấm lại** từng cặp (query, chunk) và **đổi thứ tự**.
5. Vì nếu không lọc, retrieval trả tài liệu người hỏi không được xem; LLM02 Sensitive Information Disclosure (và LLM08 Hidden Context Exposure):2026.

</details>
