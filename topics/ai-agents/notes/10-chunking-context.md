# 10. ✂️ Chunking & quản lý context

> **Một câu:** Chunking quyết định "đơn vị tri thức" mà retriever tìm được; context budget quyết định bao nhiêu trong số đó thật sự lọt vào mắt model.

## Analogy SRE

Chunk như kích thước block khi index log: quá to thì tìm ra cả đống không liên quan, quá nhỏ thì mất ngữ cảnh dòng trước/sau. Context budget như giới hạn payload của một API.

## Cốt lõi (đã kiểm chứng)

- `SentenceSplitter(chunk_size, chunk_overlap)`: cắt theo token, ưu tiên ranh giới câu.
  - ⚠️ **Docs ghi overlap mặc định 20, code chạy ra 200**: `SentenceSplitter()` → `1024 / 200`, `Settings.chunk_overlap = 200`; số 20 là hằng `DEFAULT_CHUNK_OVERLAP` (llama-index-core 0.14.25). Bài học: in ra giá trị thật.
- Docs: chunk nhỏ → embedding **chính xác hơn**, chunk lớn → **khái quát hơn** nhưng dễ mất chi tiết (*Basic strategies* § Chunk sizes).
- `SemanticSplitterNodeParser(buffer_size=1, breakpoint_percentile_threshold=95, embed_model=...)`: gom câu theo nhóm, đo khoảng cách embedding giữa các nhóm liền kề, **cắt ở chỗ khoảng cách vượt percentile 95**. Cần gọi embedding lúc ingest nên chậm hơn.
- Overlap giúp không mất ý ở mép chunk, nhưng gây **trùng lặp** trong context (khoá học nói đúng điểm này).
- Ollama: context length mặc định theo VRAM (< 24 GiB → 4k), docs khuyên agent ≥ 64000 (`docs/context-length.mdx`). Context vượt mức thì phần đầu bị cắt.
- Chiến lược khi vượt ngân sách: **lọc** (cutoff / top-k nhỏ hơn) → **cắt** (truncate theo token) → **tóm tắt** (tốn thêm một lần gọi LLM). Đo token bằng `prompt_eval_count`.

## Trong lab

Buổi 32 quét chunk size → 33 semantic chunking → 34 context budget.

## Ghi chú của tôi

## Câu hỏi còn mở

-
