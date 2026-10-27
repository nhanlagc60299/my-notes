# 2. 🛠️ Tools / Capabilities — tay chân của agent

> **Một câu:** Model **không chạy** tool — nó chỉ trả về *ý định* gọi tool (`tool_calls` gồm tên + arguments); code của mình chạy hàm thật rồi trả kết quả lại bằng message `role: "tool"`.

## Analogy SRE

Như **ChatOps bot**: người gõ `/runbook KubePodCrashLooping`, bot mới là thứ thực thi. LLM là người gõ lệnh, còn mình là bot, nên mình quyết định lệnh nào được phép chạy (allow-list), chạy với quyền gì.

## Cốt lõi (đã kiểm chứng)

- Ollama Python: truyền **hàm Python có docstring** thẳng vào `tools=[fn]`; SDK sinh JSON schema từ signature + docstring. Kết quả gửi lại dạng `{'role': 'tool', 'tool_name': ..., 'content': str(result)}`. — [Ollama Tool calling](https://docs.ollama.com/capabilities/tool-calling)
- **Agent loop** chính thức: `while True` → `chat(...)` → append `response.message` → nếu có `tool_calls` thì chạy và append kết quả → nếu không thì `break`. Docs gợi ý nói cho model biết nó đang ở trong loop và được gọi nhiều tool. — cùng trang, mục *Multi-turn tool calling (Agent loop)*
- **ACI (agent–computer interface)**: đầu tư vào mô tả tool như đầu tư vào UX; *"Poka-yoke your tools"*: đổi tham số để khó dùng sai (vd: bắt buộc absolute path). — Anthropic BEA, *Appendix 2: Prompt engineering your tools*
- **MCP**: giao thức client–server (JSON-RPC) để chuẩn hoá cách app AI lấy context/tool. Server cung cấp 3 primitive: **Tools** (hành động), **Resources** (dữ liệu), **Prompts** (template). Client khám phá bằng `tools/list`, gọi bằng `tools/call`. — [MCP Architecture](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture), [Tools spec 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- MCP spec: vì an toàn, **SHOULD luôn có người trong vòng lặp** có quyền từ chối lời gọi tool. — Tools spec § User Interaction Model
- ⚠️ MCP Python SDK **2.x**: `FastMCP` → `MCPServer` (`from mcp.server.mcpserver import MCPServer`). Tutorial cũ sẽ lỗi import.

## Trong lab

Buổi 5 một tool → 6 agent loop → 7 thiết kế tool → 8 MCP server.

## Ghi chú của tôi

<!-- tool nào model hay gọi sai? docstring nào làm nó gọi đúng? -->

## Câu hỏi còn mở

-
