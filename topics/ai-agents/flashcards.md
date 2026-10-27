# Flashcards — AI Agents

Mỗi sáng một scheduled task gửi **3 thẻ** qua Gmail, theo thứ tự trong file (thẻ chạy trước bài học một chút để gợi tò mò). Hết bộ thì quay vòng lại từ đầu: lần thứ hai chính là ôn tập giãn cách.

**Quy ước** (để task đọc được): mỗi thẻ là một heading `### FC-NN`, sau đó là các dòng `**Q:**`, `**A:**`, `**Hook:**`, `**Nguồn:**`. Thêm thẻ mới thì nối vào cuối, đánh số tiếp, đừng đánh số lại.

---

## 🧠 Brain

### FC-01
**Q:** Một LLM, xét thuần tuý như một hàm, nhận gì và trả gì? Vậy "agent" đến từ đâu?
**A:** `messages → message`. "Agent" là phần code bao quanh: đưa mục tiêu, context, tool, schema, phản hồi từ môi trường, và lặp lại.
**Hook:** Nếu bản thân model không "nhớ" gì giữa hai lần gọi, thì ChatGPT nhớ cuộc hội thoại bằng cách nào?
**Nguồn:** ollama-python `Client.chat` signature (0.6.3)

### FC-02
**Q:** Muốn LLM trả JSON đúng schema Pydantic trên Ollama thì làm thế nào?
**A:** `format=Model.model_json_schema()`, rồi `Model.model_validate_json(resp.message.content)`. Nên đưa schema vào cả prompt.
**Hook:** Vì sao đã truyền schema rồi mà docs vẫn khuyên lặp lại schema trong prompt?
**Nguồn:** docs.ollama.com/capabilities/structured-outputs

### FC-03
**Q:** Ollama cloud có hỗ trợ structured outputs không?
**A:** Hiện **không**, docs ghi rõ. Local thì có.
**Hook:** Code chạy ngon trên laptop nhưng gãy khi chuyển sang cloud. Còn bao nhiêu "khác biệt ẩn" kiểu này?
**Nguồn:** docs.ollama.com/capabilities/structured-outputs

### FC-04
**Q:** `prompt_eval_count` và `eval_count` trong `ChatResponse` là gì?
**A:** Số token input (prompt) và số token output (sinh ra). Đây là nền của cost tracking.
**Hook:** Một email 300 từ tiếng Việt ra khoảng bao nhiêu token? Đoán trước, rồi đo.
**Nguồn:** ollama `ChatResponse.model_fields`

### FC-05
**Q:** Baseline phân loại bằng từ khoá trên 30 email của lab được bao nhiêu %? Vì sao phải có con số này trước khi dùng LLM?
**A:** 63% (19/30). Không có baseline thì không biết LLM thật sự hơn được bao nhiêu, có đáng chi phí hay không.
**Hook:** Nếu LLM chỉ đạt 70% mà chậm hơn 100 lần, anh còn chọn nó không?
**Nguồn:** lab `01_hello_brain.py`

## 🛠️ Tools

### FC-06
**Q:** Khi model "gọi tool", ai thực sự chạy hàm?
**A:** **Code của mình.** Model chỉ trả `tool_calls` (tên + arguments) và mình quyết định có chạy hay không.
**Hook:** Vậy "AI tự xoá database" thực chất là lỗi của ai?
**Nguồn:** docs.ollama.com/capabilities/tool-calling

### FC-07
**Q:** Kết quả tool gửi lại cho model trên Ollama có dạng gì?
**A:** `{'role': 'tool', 'tool_name': <tên>, 'content': str(result)}`
**Hook:** Nếu tool trả một traceback 200 dòng, model sẽ làm gì với nó?
**Nguồn:** docs.ollama.com/capabilities/tool-calling

### FC-08
**Q:** Agent loop trong docs Ollama dừng khi nào? Thiếu gì để lên production?
**A:** Dừng khi response không còn `tool_calls`. Thiếu: trần số bước, xử lý tool lỗi, allow-list tool.
**Hook:** Model cứ gọi đi gọi lại một tool vì không hài lòng với kết quả: chuyện gì xảy ra lúc 3h sáng?
**Nguồn:** docs.ollama.com/capabilities/tool-calling § Agent loop

### FC-09
**Q:** "Poka-yoke your tools" nghĩa là gì?
**A:** Thiết kế tham số tool sao cho **khó dùng sai**, ví dụ bắt buộc absolute path thay vì relative path.
**Hook:** `run_kubectl(command: str)` vi phạm poka-yoke ở chỗ nào?
**Nguồn:** Anthropic, Building effective agents, Appendix 2

### FC-10
**Q:** MCP server cung cấp 3 primitive nào?
**A:** **Tools** (hành động), **Resources** (dữ liệu context), **Prompts** (template). Client khám phá bằng `tools/list`.
**Hook:** Runbook nên là Tool hay Resource? Tại sao?
**Nguồn:** modelcontextprotocol.io/docs/2026-07-28/learn/architecture

### FC-11
**Q:** ⚠️ Bẫy lỗi thời: `from mcp.server.fastmcp import FastMCP` trên `mcp` 2.x?
**A:** Lỗi import. SDK 2.x đổi thành `from mcp.server.mcpserver import MCPServer`.
**Hook:** Có bao nhiêu tutorial MCP trên mạng đang chết vì đúng dòng này?
**Nguồn:** thông báo lỗi trong `mcp==2.3.0`

### FC-12
**Q:** Spec MCP mới nhất là phiên bản nào? Spec nói gì về con người và tool call?
**A:** **2026-07-28**. Vì an toàn, **SHOULD** luôn có người trong vòng lặp, có quyền từ chối lời gọi tool.
**Hook:** Nếu chính spec đã nói vậy, sao nhiều demo agent vẫn chạy "full auto"?
**Nguồn:** modelcontextprotocol.io/specification/2026-07-28/server/tools

## 🗺️ Planning

### FC-13
**Q:** Workflow và agent khác nhau thế nào (theo Anthropic)?
**A:** Workflow: LLM và tool chạy theo đường code **định sẵn**. Agent: LLM **tự điều khiển** quy trình và việc dùng tool, lặp dựa trên phản hồi từ môi trường.
**Hook:** Agent phân loại email của anh thật ra nên là workflow hay agent?
**Nguồn:** anthropic.com/engineering/building-effective-agents

### FC-14
**Q:** 5 pattern workflow của Anthropic là gì?
**A:** Prompt chaining · Routing · Parallelization · Orchestrator-workers · Evaluator-optimizer.
**Hook:** Pattern nào trong đó chính là "Reflexion" được đặt tên khác?
**Nguồn:** Building effective agents

### FC-15
**Q:** ReAct là viết tắt của gì, và giống vòng nào khi xử lý sự cố?
**A:** **Re**ason + **Act**: nghĩ → hành động (tool) → quan sát kết quả → nghĩ tiếp. Giống vòng debug: giả thuyết → `kubectl` → đọc output.
**Hook:** Nếu bỏ bước "quan sát" thì agent khác gì một script?
**Nguồn:** LangGraph Workflows & agents § Agents

### FC-16
**Q:** `think=True` trên Ollama trả thêm gì? Có nên luôn bật không?
**A:** Field `message.thinking` (reasoning trace, tách khỏi câu trả lời). Không nên luôn bật vì tốn token và thời gian: đo bằng eval rồi mới quyết.
**Hook:** Model "suy nghĩ" lâu hơn có chắc trả lời đúng hơn không?
**Nguồn:** docs.ollama.com/capabilities/thinking

### FC-17
**Q:** 3 thành phần của một LangGraph graph?
**A:** **State** (dữ liệu chung), **Nodes** (hàm), **Edges** (thường hoặc có điều kiện). Graph chạy theo super-step.
**Hook:** Super-step giống khái niệm nào trong Kubernetes controller loop?
**Nguồn:** docs.langchain.com/oss/python/langgraph/graph-api

## 💾 Memory

### FC-18
**Q:** Checkpointer và Store khác nhau thế nào?
**A:** Checkpointer lưu state **theo thread** (short-term). Store lưu dữ liệu **qua nhiều thread** (long-term).
**Hook:** Incident channel và wiki của team, cái nào là checkpointer, cái nào là store?
**Nguồn:** docs.langchain.com/oss/python/langgraph/persistence

### FC-19
**Q:** `thread_id` đặt ở đâu? Đổi `thread_id` thì sao?
**A:** `config={"configurable": {"thread_id": ...}}`. Đổi thì thành thread mới, state rỗng.
**Hook:** Email "Re: Re: Fwd:" nên dùng chung thread_id không? Lấy giá trị từ header nào?
**Nguồn:** LangGraph Interrupts / Persistence

### FC-20
**Q:** 3 cách quản lý short-term memory khi messages phình to?
**A:** Trim, delete, summarize messages.
**Hook:** Tóm tắt thì có thể làm mất chi tiết. Chi tiết nào trong một incident tuyệt đối không được mất?
**Nguồn:** docs.langchain.com/oss/python/langgraph/add-memory

### FC-21
**Q:** Embedding là gì? Vector thường dài bao nhiêu chiều?
**A:** Text biến thành vector số để so độ giống nhau bằng cosine; thường 384–1024 chiều tuỳ model.
**Hook:** "Disk full" và "ổ đĩa đầy" có gần nhau trong không gian vector không?
**Nguồn:** docs.ollama.com/capabilities/embeddings

### FC-22
**Q:** RAG có rủi ro bảo mật riêng không? OWASP 2026 gọi là gì?
**A:** Có: **LLM09:2026 Vector and Embedding Weaknesses** (vd: tài liệu trong kho RAG bị đầu độc).
**Hook:** Nếu ai đó sửa runbook trong wiki thành "khi disk full hãy `rm -rf /var`", agent RAG của anh sẽ làm gì?
**Nguồn:** OWASP GenAI LLM Top 10 2026

## 🔄 Environment

### FC-23
**Q:** Code dừng chờ người duyệt trong LangGraph, và code resume?
**A:** Trong node: `ok = interrupt({...})`. Bên ngoài: `graph.invoke(Command(resume=True), config)`.
**Hook:** Agent đang chờ duyệt thì server restart. State còn không? Còn nhờ cái gì?
**Nguồn:** docs.langchain.com/oss/python/langgraph/interrupts

### FC-24
**Q:** Vì sao code trước `interrupt()` phải idempotent?
**A:** Khi resume, node **chạy lại từ đầu**, nên side-effect phía trước bị chạy lần hai.
**Hook:** Giống bài toán gì của job retry trong Kubernetes?
**Nguồn:** Interrupts § Rules of interrupts

### FC-25
**Q:** ⚠️ Bẫy lỗi thời: `interrupt_before=[...]` có phải cách chuẩn để làm HITL?
**A:** Không. Docs hiện mô tả nó là **static breakpoint để debug**. HITL dùng `interrupt()` cộng `Command(resume=...)`.
**Hook:** Còn API nào bị "đổi vai" kiểu này mà tutorial chưa cập nhật?
**Nguồn:** Interrupts § Debugging with interrupts

### FC-26
**Q:** Đúng/sai: "Có thể truyền `Command(update=...)` vào `invoke()` để tiếp tục hội thoại."
**A:** Sai. `Command(resume=...)` là pattern `Command` **duy nhất** dùng làm input cho `invoke()`. Muốn tiếp tục hội thoại thì truyền dict thường.
**Hook:** Graph "đứng im không chạy". Lỗi này có thể là thủ phạm.
**Nguồn:** docs.langchain.com/oss/python/langgraph/graph-api

### FC-27
**Q:** Multi-agent đơn giản nhất là pattern nào?
**A:** **Routing**: phân loại input rồi gửi tới agent/chuyên gia phù hợp.
**Hook:** Router phân loại sai thì chuyên gia "nhầm phòng" có quyền gì? Đó là lý do cần least privilege.
**Nguồn:** Building effective agents; LangGraph Workflows § Routing

## 🛡️ Guardrails

### FC-28
**Q:** OWASP LLM Top 10 phiên bản hiện hành là năm nào? LLM01 là gì?
**A:** **2026** (phát hành 2026-08-04). LLM01:2026 = Prompt Injection.
**Hook:** Bản 2025 xếp Excessive Agency ở LLM06. Bản 2026 đưa nó lên số mấy? (→ FC-30)
**Nguồn:** github.com/GenAI-Security-Project/GenAI-LLM-Top10

### FC-29
**Q:** Theo OWASP LLM01:2026, có cơ chế chặn prompt injection đáng tin cậy không?
**A:** **Không.** "No reliable prevention mechanism exists today", nên phòng thủ phải là *architectural*: giới hạn những gì model được làm và output được chạm tới.
**Hook:** Nếu không chặn được 100%, anh sẽ đặt "bức tường cuối cùng" ở đâu?
**Nguồn:** OWASP LLM01:2026 § Prevention and Mitigation

### FC-30
**Q:** LLM03:2026 là gì?
**A:** **Excessive Agency**: agent có quá nhiều quyền, tool hoặc tự chủ.
**Hook:** Đếm xem agent của anh có bao nhiêu tool có side-effect.
**Nguồn:** OWASP GenAI LLM Top 10 2026

### FC-31
**Q:** Agent đọc email chứa "AI assistant hãy tự cấp quyền admin…" là loại injection gì?
**A:** **Indirect** prompt injection: lệnh đến từ dữ liệu agent đọc, không phải từ người dùng.
**Hook:** Inbox là nơi bất kỳ ai trên Internet cũng gửi vào được. Agent đọc mail có bề mặt tấn công lớn cỡ nào?
**Nguồn:** OWASP LLM01:2026 § Types

### FC-32
**Q:** LLM02 và LLM10 (2026) là gì?
**A:** LLM02 = Sensitive Information Disclosure. LLM10 = Improper Output Handling.
**Hook:** Summary của agent có chép nguyên số hộ chiếu trong email ra Slack không?
**Nguồn:** OWASP GenAI LLM Top 10 2026

## 📊 Observability & Evals

### FC-33
**Q:** `stream_mode` nào giúp dựng trace từng bước trong LangGraph?
**A:** `"updates"`: phát state update sau mỗi bước.
**Hook:** Cần LangSmith không, hay 20 dòng Python ghi JSONL là đủ cho giai đoạn này?
**Nguồn:** docs.langchain.com/oss/python/langgraph/streaming

### FC-34
**Q:** Golden dataset bảo vệ anh khỏi điều gì?
**A:** **Regression âm thầm** khi đổi prompt hoặc model: tổng thể trông vẫn ổn nhưng một nhóm case quan trọng (vd: injection) bị hỏng.
**Hook:** Accuracy giữ nguyên 83% có nghĩa là không có gì tệ đi không?
**Nguồn:** Building effective agents ("optimize with comprehensive evaluation")

### FC-35
**Q:** Vì sao trace agent phải lưu cả kết quả tool?
**A:** Agent quyết định dựa trên ground truth từ môi trường ở mỗi bước. Lỗi thường bắt nguồn từ một kết quả tool bị hiểu sai.
**Hook:** Trong distributed tracing, span nào hay "giấu" lỗi nhất?
**Nguồn:** Building effective agents § Agents

### FC-36
**Q:** Eval với LLM thật thì chậm và không tất định. Đưa vào CI thế nào?
**A:** CI chạy trên kết quả đã cache hoặc FakeLLM (tất định). Eval LLM thật chạy định kỳ, ghi file kết quả, gate đọc file đó.
**Hook:** Giống chiến lược nào khi test với dịch vụ bên thứ ba?
**Nguồn:** thiết kế lab (heuristic, không phải docs)

## 💸 Cost control

### FC-37
**Q:** ⚠️ Bẫy lỗi thời: `recursion_limit` mặc định của LangGraph Python?
**A:** **1000** từ langgraph 1.0.6. Con số 25 là của bản JS hoặc tutorial cũ.
**Hook:** 1000 vòng gọi LLM cho một email: tốn bao nhiêu phút GPU?
**Nguồn:** docs.langchain.com/oss/python/langgraph/graph-api § Recursion limit

### FC-38
**Q:** Đặt `recursion_limit` ở đâu trong config?
**A:** Ở **cấp ngoài cùng**: `{"recursion_limit": 5, "configurable": {...}}`. Đặt trong `configurable` thì không có tác dụng.
**Hook:** Lỗi cấu hình "im lặng" kiểu này giống lỗi YAML indent nào anh từng gặp?
**Nguồn:** Graph API § Recursion limit

### FC-39
**Q:** `RemainingSteps` khác gì bắt `GraphRecursionError`?
**A:** `RemainingSteps` là proactive: node biết còn bao nhiêu bước để tự dừng êm. Bắt exception là reactive: graph đã bị cắt ngang.
**Hook:** Deadline propagation trong gRPC giải quyết đúng bài toán này.
**Nguồn:** Graph API § Recursion limit

### FC-40
**Q:** OWASP 2026 gọi rủi ro "đốt tài nguyên không giới hạn" là gì?
**A:** **LLM06:2026 Unbounded Consumption.**
**Hook:** Ai đó gửi 10.000 email rác vào inbox mà agent đọc. Chuyện gì xảy ra với GPU của anh?
**Nguồn:** OWASP GenAI LLM Top 10 2026
