# Quiz 2 — 🛠️ Tools & MCP

**Pass:** ≥ 4/5 câu A **và** phần C xanh.

## A. Kiến thức

1. Khi model "gọi tool", **ai** thực sự chạy hàm? Model trả về cái gì?
2. Kết quả tool được gửi lại cho model dưới dạng message có `role` gì và field nào chứa tên tool (Ollama)?
3. Trong agent loop của docs Ollama, **điều kiện dừng** là gì? Điều gì còn thiếu nếu đem chạy production?
4. MCP server cung cấp 3 primitive nào? Client dùng method nào để khám phá tool?
5. Code `from mcp.server.fastmcp import FastMCP` lỗi với `mcp==2.3.0`. Vì sao, và sửa thế nào?

## B. Tình huống

Anh cho agent tool `run_kubectl(command: str)`. Áp nguyên tắc **poka-yoke** (Anthropic, Appendix 2) và **least privilege**: thiết kế lại tool này thành 1–3 tool an toàn hơn. Viết signature + docstring.

## C. Thực hành

```bash
pytest -q tests/test_05_one_tool.py tests/test_06_agent_loop.py tests/test_08_mcp_server.py
```

<details><summary>Đáp án A</summary>

1. **Code của mình** chạy hàm. Model chỉ trả `message.tool_calls` = danh sách `{function: {name, arguments}}`.
2. `{'role': 'tool', 'tool_name': <tên>, 'content': str(result)}`.
3. Dừng khi response **không còn `tool_calls`**. Thiếu **trần số bước** (max loop/`recursion_limit`), xử lý tool lỗi, allow-list tên tool.
4. **Tools, Resources, Prompts**; khám phá bằng `tools/list` (gọi bằng `tools/call`).
5. SDK 2.x đổi tên `FastMCP` → `MCPServer`: `from mcp.server.mcpserver import MCPServer` (hoặc pin `mcp<2` nếu giữ code v1).

</details>

<details><summary>Gợi ý B</summary>

Thay 1 tool "làm được mọi thứ" bằng tool hẹp, tham số có kiểu: `get_pod_status(namespace: Literal[...], pod: str)`, `get_pod_logs(namespace, pod, tail: int <= 200)`, đều **read-only**; hành động ghi (restart) tách riêng và đi qua HITL. Docstring nói rõ khi nào dùng, ví dụ input, và lỗi trả về trông thế nào.

</details>
