# 7. 📊 Observability & Evaluation — nhìn thấy và chấm điểm

> **Một câu:** **Tracing** trả lời "agent đã làm *gì*, theo *thứ tự nào*, *tốn bao nhiêu*"; **Evals** trả lời "nó làm *đúng* không, và lần đổi prompt/model này có làm nó *tệ đi* không".

## Analogy SRE

- Trace agent = **distributed trace**: mỗi node/tool call là 1 span (tên, input, output, latency, token).
- Golden dataset + eval = **SLO + regression test** cho chất lượng: đổi model mà accuracy tụt dưới ngưỡng thì chặn ở CI, như canary fail.

## Cốt lõi (đã kiểm chứng)

- LangGraph streaming: `stream_mode="updates"` phát state update sau **mỗi bước** → đủ để tự dựng trace JSONL không cần SaaS. — [Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)
- Anthropic BEA: ưu tiên **transparency**, hiển thị rõ các bước planning của agent; *"optimize [prompts] with comprehensive evaluation"*.
- Agent cần *ground truth từ môi trường mỗi bước* (kết quả tool) → trace phải lưu **cả kết quả tool**, không chỉ output cuối.
- LangSmith / Phoenix là công cụ trace chuyên dụng → **để dành cho 20h #2 (OpenTelemetry)**: Phoenix dựa trên OTel, nên sẽ nối thẳng sang chủ đề sau. ⚠️ chưa kiểm chứng chi tiết tích hợp, sẽ kiểm ở 20h #2.

## Trong lab

Buổi 23 trace JSONL → 24 eval gate trong pytest.

## Ghi chú của tôi

## Câu hỏi còn mở

-
