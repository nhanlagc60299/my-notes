# Quiz 3 — 🗺️ Planning & Reasoning

**Pass:** ≥ 4/5 câu A **và** phần C xanh.

## A. Kiến thức

1. Phân biệt **workflow** và **agent** theo Anthropic trong 1 câu mỗi cái.
2. Kể tên 5 pattern workflow trong *Building effective agents*. Pattern nào là nền của Reflexion/self-correction?
3. 3 thành phần của một LangGraph graph là gì? Edge có điều kiện dùng để làm gì trong ReAct graph?
4. Bật `think=True` trên Ollama thì response có thêm field nào? Chi phí của nó là gì?
5. Vòng validate → retry của anh chạy mãi vì model luôn trả sai schema. Hai cơ chế nào chặn được chuyện này?

## B. Tình huống

Vẽ (Mermaid hoặc giấy) graph của agent hiện tại: node nào, edge nào, điều kiện nào dẫn tới `END`. So với output của `graph.get_graph().draw_mermaid()`, chỗ nào khác với hình anh nghĩ trong đầu?

## C. Thực hành

```bash
pytest -q tests/test_11_react_graph.py tests/test_12_reflexion.py
```

<details><summary>Đáp án A</summary>

1. Workflow: LLM + tool chạy theo **đường code định sẵn**. Agent: LLM **tự điều khiển** quy trình và việc dùng tool, lặp dựa trên phản hồi môi trường.
2. Prompt chaining, Routing, Parallelization, Orchestrator-workers, **Evaluator-optimizer** (nền của Reflexion).
3. **State, Nodes, Edges.** Conditional edge quyết định đi tới node `tools` (khi có tool_calls) hay `END`.
4. Field `message.thinking`. Chi phí: thêm token + thời gian, nên phải đo bằng eval xem có đáng không.
5. Đếm số lần retry trong state (tối đa N rồi trả lỗi có kiểm soát / chuyển người) **và** `recursion_limit` làm lưới an toàn.

</details>
