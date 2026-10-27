# Kiểm chứng: khoá "GenAI Model Access Layer and Structured Outputs"

> Tài liệu tham khảo cho Phần A (Brain, Tools, Guardrails, Cost) và Khối 14. Không lưu nguyên transcript, chỉ lưu kết quả đối chiếu.
> Kiểm chứng ngày **2026-10-28** trên: SDK chính thức đã cài và đọc kiểu dữ liệu (`openai 3.40.0`, `ollama 0.6.3`), tài liệu tham chiếu Claude API chính thức (skill `claude-api`, bản cache 2026-10-06), docs Hugging Face PEFT (GitHub), và các review trước của repo.

**Kết luận nhanh:** Phần **kỹ thuật vận hành** của khoá đúng và thực dụng: client wrapper thống nhất, timeout/retry/backoff + jitter, phân loại lỗi, fallback model, validate output bằng schema, retry kèm thông báo lỗi cụ thể, prompt versioning, A/B test, test edge case và prompt injection, gói lỗi tool thành cấu trúc, kiểm quyền trước khi chạy tool. Nhưng phần **API của nhà cung cấp đã lỗi thời hoặc mô tả nhầm** ở 4 chỗ quan trọng: JSON mode bị nhầm với Structured Outputs, "prompt caching" bị nhầm với response cache, batching bị mô tả sai, và cách lấy structured output từ Claude đã có cách mới chuẩn hơn tool use.

## Bảng đối chiếu

Ký hiệu: ✅ đúng · ⚠️ đúng một phần / cần chỉnh · ❌ sai · 🕐 lỗi thời

| # | Khoá học nói | Kết quả | Sự thật & nguồn |
|---|---|---|---|
| 1 | API key không hard-code, dùng secret manager/biến môi trường, xoay vòng key, scope hẹp | ✅ | Thực hành chuẩn |
| 2 | Bọc mọi provider sau một client wrapper thống nhất (auth, retry, timeout, streaming, lỗi) | ✅ | Đúng; lab đã làm dạng tối giản ở `llm.py` (factory Fake/Ollama cùng kiểu trả về) |
| 3 | Retry chỉ lỗi tạm thời, backoff + jitter, giới hạn số lần; lỗi client/auth thì fail nhanh | ✅ | Khớp review khoá SLO. Thêm: SDK Anthropic mặc định `max_retries=2` (retry 408/409/429/5xx + lỗi kết nối) và timeout mặc định 10 phút. Timeout cũng được retry, nên thời gian thực có thể tới `timeout × (max_retries+1)` (tài liệu Claude API) |
| 4 | Đặt timeout connect / read / tổng | ✅ | Thực hành chuẩn (httpx có `connect/read/write/pool`) |
| 5 | **"Prompt caching"** = lưu cặp prompt → response ở tầng ứng dụng để trả lại ngay | ❌ **nhầm thuật ngữ** | **Prompt caching của nhà cung cấp** (Anthropic, OpenAI) cache **tiền tố prompt** (prefix) phía server để giảm chi phí và độ trễ **đầu vào**; model **vẫn sinh câu trả lời mới**. Anthropic: `cache_control: {"type": "ephemeral"}` (TTL 5 phút mặc định, hoặc `"ttl": "1h"`); đọc cache ≈ 0,1× giá input (thấp hơn trên một số model mới); khớp theo **prefix**, đổi một byte là mất cache phía sau. Thứ khoá học mô tả là **response cache** của ứng dụng (đã học ở Khối 14: key phải có tenant + version). OTel GenAI semconv cũng tách riêng `…cache_read.input_tokens` / `…cache_write.input_tokens` |
| 6 | **Batching** = "gộp nhiều prompt vào **một** API call" | ⚠️ / ❌ | **Batch API** của nhà cung cấp là **job bất đồng bộ**: gửi nhiều request độc lập, kết quả trả về sau. Anthropic Message Batches: **giảm 50%** chi phí, đa số xong trong 1 giờ, **tối đa 24 giờ**, kết quả **không theo thứ tự** (khớp bằng `custom_id`). OpenAI: `client.batches`, `completion_window="24h"` (kiểu dữ liệu SDK 3.40.0). Không phải nhét nhiều prompt vào một lời gọi |
| 7 | Streaming cải thiện độ trễ cảm nhận; xử lý stream bị cắt giữa chừng | ✅ | Đúng. Với Claude, tài liệu khuyên **stream** cho output dài/`max_tokens` lớn để tránh timeout HTTP |
| 8 | Thiết kế JSON schema: liệt kê field, kiểu, required, min/max, enum; validate bằng Pydantic/JSON Schema; lỗi thì retry/sửa/fallback | ✅ | Khớp Buổi 2 (Ollama `format=Model.model_json_schema()` + `model_validate_json`) |
| 9 | **"OpenAI JSON mode"**: định nghĩa đúng cấu trúc JSON với field required + giá trị cho phép, model bị ép trả đúng schema | ❌ 🕐 **nhầm hai tính năng** | **JSON mode** (`response_format={"type": "json_object"}`) chỉ bảo đảm **JSON hợp lệ**, **không** bảo đảm schema. Docstring SDK: *"An older method of generating JSON responses. Using `json_schema` is recommended… the model will not generate JSON without a system or user message instructing it to do so."* Cái khoá mô tả là **Structured Outputs**: `response_format={"type": "json_schema", "json_schema": {"name", "schema", "strict": true}}`, hoặc helper `client.chat.completions.parse(...)` / `client.responses.parse(...)`. Model có thể trả `refusal` thay vì JSON |
| 10 | Claude: dùng **tools** để lấy output có cấu trúc | 🕐 | Vẫn chạy được, nhưng Claude API hiện có **Structured Outputs native**: `output_config: {format: {...}}` (tham số cũ `output_format` đã **deprecated**), helper `client.messages.parse()`, và **strict tool use**: `strict: true` trên định nghĩa tool (không cần beta; schema cần `additionalProperties: false` + `required`). Trên các model Claude mới nhất, **forced `tool_choice` (`any`/`tool`) trả lỗi 400**, nên mẹo "ép gọi tool để lấy JSON" không còn dùng được: chuyển sang `output_config.format` |
| 11 | "Native structured output → **ít hallucination hơn nhiều**" | ⚠️ | Ràng buộc schema bảo đảm **định dạng** (đúng field, đúng kiểu, đúng enum), **không** bảo đảm **nội dung đúng**. Giá trị bên trong vẫn có thể bịa. Vẫn cần kiểm tra nghiệp vụ, đối chiếu nguồn (RAG) và guardrails |
| 12 | Lỗi output: thiếu field, sai định dạng, field bịa; sửa bằng retry **kèm lỗi cụ thể**, chỉ sửa field hỏng, default an toàn cho field ít rủi ro | ✅ | Khớp Buổi 12 (evaluator-optimizer). Lưu ý: với constrained decoding (Ollama `format`, OpenAI `strict`, Claude `output_config.format`) lỗi cú pháp hiếm hơn nhiều; vẫn phải validate vì có thể bị cắt do `max_tokens` hoặc model từ chối |
| 13 | Function calling: model chọn hàm + điền tham số; ứng dụng validate, kiểm quyền, chạy, trả kết quả | ✅ | Khớp Buổi 5–7 và FC-11. OpenAI `FunctionDefinition` có trường `strict` (SDK 3.40.0) |
| 14 | Lỗi tool trả về **có cấu trúc** (`status`, `data`, `error`, loại lỗi) để model quyết định retry / đổi tool / hỏi lại | ✅ | Thực hành tốt; với Claude, lỗi tool trả `tool_result` với `is_error: true` (tài liệu Claude API) |
| 15 | Prompt template có biến, điều kiện, chọn ví dụ động (few-shot theo độ tương tự) | ✅ | Chọn ví dụ động = episodic memory dùng làm few-shot (Buổi 45). Rủi ro: ví dụ lấy từ dữ liệu người dùng cũng là input không tin cậy |
| 16 | Prompt là code: version control, log version ở mỗi lời gọi, metric theo version, A/B test có ý nghĩa thống kê | ✅ | Bổ sung vào lab: ghi `prompt_version` vào trace (Buổi 23) và vào cache key (Buổi 49). Với golden set nhỏ (30 email), A/B **offline** trên golden set đáng tin hơn A/B traffic thật |
| 17 | Phát hiện injection bằng dấu hiệu ngôn ngữ, làm sạch input, tách vai system/developer/user; "model **luôn** coi system là bất biến, ưu tiên cao hơn" | ⚠️ | Tách vai và làm sạch là lớp phòng thủ hữu ích, nhưng OWASP LLM01:2026: **không có cơ chế ngăn chặn đáng tin cậy**; model không *bảo đảm* tuân thứ bậc chỉ dẫn. Lớp quyết định là giới hạn quyền + người duyệt (FC-29) |
| 18 | Test prompt: coverage, edge case, adversarial, đa dạng ngôn ngữ, chạy tự động trong CI/CD | ✅ | Khớp eval gate (Buổi 24). Dataset lab đã có email tiếng Việt + tiếng Anh + 3 email injection |
| 19 | Confidence qua **logprobs** và **lấy mẫu nhiều lần**; thấp thì người duyệt / chạy lại / fallback | ✅ ⚠️ | Ollama hỗ trợ `logprobs`, `top_logprobs` trong `Client.chat` (0.6.3); OpenAI có `logprobs`/`top_logprobs`. **Claude API không công bố logprobs** (không có trong tài liệu tham chiếu) ⇒ dùng self-consistency (lấy mẫu nhiều lần, so sánh). Lưu ý: logprob **không phải** độ tin cậy đã hiệu chỉnh; phải kiểm trên golden set xem ngưỡng có tách đúng/sai không |
| 20 | Validate nhiều lớp: schema, safety filter, fact-check, business rules | ✅ | Khớp Guardrails (Khối 6) |
| 21 | RAG: câu trả lời dựa trên nguồn tin cậy, "model **không bịa**", giảm hallucination | ⚠️ | RAG **giảm** chứ không **loại bỏ** hallucination (OWASP LLM07:2026 Misinformation nêu cả *weak grounding*, *stale context*). Phải đo grounding (Khối 9, FC-64) |
| 22 | Fine-tune chỉ khi cần; prompt engineering và RAG trước | ✅ | Khớp lời khuyên "bắt đầu đơn giản" (Anthropic BEA). Lab cố tình bỏ fine-tuning |
| 23 | LoRA: chèn ma trận nhỏ trainable, đóng băng trọng số gốc; QLoRA: kết hợp adapter + lượng tử hoá 4-bit | ✅ | Docs Hugging Face PEFT: `LoraConfig` + `get_peft_model` (ví dụ chỉ train ~0,19% tham số); hướng dẫn quantization: `load_in_4bit=True`, `bnb_4bit_quant_type="nf4"` qua bitsandbytes |
| 24 | Multimodal: ảnh được quy ra token theo độ phân giải; giảm độ phân giải/crop để tiết kiệm; fallback OCR khi vision kém | ✅ | Tài liệu Claude API: token ảnh tỉ lệ theo diện tích pixel (khoảng 1 token / ô 28×28), nên giảm độ phân giải trước khi gửi. Ollama nhận ảnh qua trường `images` của message. Nằm ngoài phạm vi lab (cố tình bỏ) |
| 25 | Ví dụ demo gọi OpenAI bằng `requests` thô + cache dict trong RAM | ⚠️ | Chỉ để minh hoạ. Production nên dùng SDK chính thức (có sẵn retry, timeout, kiểu lỗi), và cache có TTL + key gồm model/prompt version/tenant |

## Áp vào lab (không tăng giờ)

| Ý từ khoá | Buổi | Thay đổi |
|---|---|---|
| Structured output đúng cách | 2 | Ollama `format=<schema>`, ghi chú tương đương: OpenAI `json_schema` + `strict`; Claude `output_config.format` / `messages.parse()`. **Không** dùng JSON mode khi cần schema |
| Retry kèm lỗi cụ thể, chỉ sửa field hỏng | 12 | Node `validate` trả lỗi Pydantic chi tiết vào lần sửa |
| Lỗi tool có cấu trúc + kiểm quyền | 7, 21 | Tool trả `{status, data, error: {type, message}}`; allow-list theo nhánh |
| Prompt versioning | 3, 23, 49 | `PROMPT_VERSION` trong code; ghi vào trace và cache key; so sánh version trên golden set |
| Confidence | 10, 52 | Thử `logprobs=True` của Ollama trên nhãn; kiểm xem ngưỡng có tách đúng/sai trên golden set không, nếu có thì dùng làm tín hiệu `needs_human` |
| Provider prompt caching vs response cache | 49 | Phân biệt rõ hai loại; Ollama local giữ model trong RAM theo `keep_alive`, không có tính phí cache |

## Nguồn

- OpenAI Python SDK `openai 3.40.0` (đã cài, đọc kiểu): `ResponseFormatJSONObject` (docstring "An older method…"), `ResponseFormatJSONSchema.JSONSchema` (`name`, `schema`, `strict`), `chat.completions.parse`, `responses.parse`, `batches` (`completion_window="24h"`), `ChatCompletionMessage.refusal`, `FunctionDefinition.strict`, tham số `logprobs`/`top_logprobs`
- Tài liệu tham chiếu Claude API chính thức (skill `claude-api`): Structured Outputs (`output_config.format`, `output_format` deprecated, `messages.parse()`, `strict: true`), forced `tool_choice` bị từ chối trên model mới, Prompt caching (`cache_control`, TTL 5m/1h, đọc ≈ 0,1×), Message Batches (50%, tối đa 24h, `custom_id`), cấu hình client (`max_retries=2`, timeout 10 phút), token ảnh
- `ollama 0.6.3`: `Client.chat(..., logprobs, top_logprobs, format, ...)`, `Message.images`
- Hugging Face PEFT: `README.md`, `docs/source/developer_guides/quantization.md`
- OWASP GenAI LLM Top 10 2026 (LLM01, LLM07)
