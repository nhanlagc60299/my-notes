"""In trạng thái học hiện tại, ngắn gọn, để một session Claude mới biết ngay phải dạy gì.

    python3 scripts/status.py            # chủ đề 🟢 trong learning/README.md
    python3 scripts/status.py ai-agents

SessionStart hook (.claude/hooks/session-start.sh) gọi script này; output được đưa vào
ngữ cảnh của session. Chỉ đọc file, không chạy test, không cần dependency ngoài stdlib.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from progress import LEARNING, REPO, active_topic, plan_file, topic_bar  # noqa: E402


def log_rows(plan_text: str) -> list[list[str]]:
    log = plan_text.split("## Log", 1)[-1].split("\n## ", 1)[0]
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in log.splitlines() if l.startswith("|")]
    return [r for r in rows if r and re.match(r"\d", r[0])]


def next_tests(topic: str) -> list[str]:
    found = []
    for f in sorted((REPO / "topics" / topic / "lab" / "tests").glob("test_*.py")):
        found += [f"{f.name}::{m}" for m in re.findall(r"@pytest\.mark\.next\s*\n\s*def (\w+)", f.read_text(encoding="utf-8"))]
    return found


def wrong_questions(topic: str) -> list[str]:
    out = []
    for f in sorted((REPO / "topics" / topic / "notebook").glob("[0-9][0-9]-*.md")):
        out += [f"{f.name}: {q.strip()}" for q in re.findall(r"^### \d+\. ❌ (.+)$", f.read_text(encoding="utf-8"), flags=re.M)]
    return out


def status(topic: str) -> str:
    plan = plan_file(topic)
    text = plan.read_text(encoding="utf-8")
    lines = [f"## Trạng thái học (my-notes) · chủ đề: {topic}", f"- Lộ trình: {plan.relative_to(REPO)}"]
    for label in ("Buổi kế", "Bước tiếp theo"):
        m = re.search(rf"^> \*\*{label}:?\s*(.*)$", text, flags=re.M)
        if m:
            lines.append(f"- {label}: " + re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", m.group(1)).replace("**", "").strip())
    lines.append(f"- Tiến độ: {topic_bar(topic).strip('`')} (giờ tích luỹ)")
    rows = log_rows(text)
    if rows:
        last = rows[-1]
        lines.append(f"- Dòng Log cuối: buổi {last[0]} · {last[1]} · pass {last[3] if len(last) > 3 else '?'} · gap: {last[4] if len(last) > 4 and last[4] else '—'}")
    tests = next_tests(topic)
    lines.append(f"- Test `next` (việc đầu tiên): {', '.join(tests) if tests else 'không có'}")
    wrong = wrong_questions(topic)
    lines.append(f"- Câu ❌ trong sổ ôn tập: {len(wrong)}" + (f" (vd: {wrong[-1]})" if wrong else ""))
    lines.append('- Làm theo CLAUDE.md: người học gõ "học tiếp" thì vào thẳng Buổi kế, khởi động bằng 2–3 câu tự nhớ lại.')
    return "\n".join(lines)


if __name__ == "__main__":
    print(status(sys.argv[1] if len(sys.argv) > 1 else active_topic((LEARNING / "README.md").read_text(encoding="utf-8"))))
