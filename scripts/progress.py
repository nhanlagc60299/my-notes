"""Thanh tiến độ theo giờ tích luỹ (không dùng streak).

    python3 scripts/progress.py               # in thanh của chủ đề đang học
    python3 scripts/progress.py ai-agents     # chủ đề cụ thể
    python3 scripts/progress.py --write       # cập nhật thanh trong README.md và file lộ trình

Giờ = số lớn nhất ở cột "Giờ tích luỹ" của bảng Log; mốc = số giờ trong tên file
learning/<topic>-<N>h.md. Thanh nằm trong code span dạng `███░░░░░░░ 6/40h`.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEARNING = REPO / "learning"
WIDTH = 10
BAR_RE = re.compile(r"`[█░]{%d} [\d.]+/\d+h`" % WIDTH)


def active_topic(queue_text: str) -> str:
    """Chủ đề có 🟢 trong hàng đợi của learning/README.md."""
    for row in queue_text.splitlines():
        m = re.search(r"\(([a-z0-9-]+)-\d+h\.md\)", row)
        if "🟢" in row and m:
            return m.group(1)
    raise SystemExit("Không thấy chủ đề 🟢 trong learning/README.md")


def plan_file(topic: str) -> Path:
    files = sorted(LEARNING.glob(f"{topic}-*h.md"))
    if not files:
        raise SystemExit(f"Không có learning/{topic}-<N>h.md")
    return files[0]


def hours_done(plan_text: str) -> float:
    log = plan_text.split("## Log", 1)[-1].split("\n## ", 1)[0]
    hours = 0.0
    for row in log.splitlines():
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.fullmatch(r"\d+(?:[.,]\d+)?", cells[2]):
            hours = max(hours, float(cells[2].replace(",", ".")))
    return hours


def bar(hours: float, target: int) -> str:
    filled = min(WIDTH, int(hours / target * WIDTH + 0.5))
    return f"`{'█' * filled}{'░' * (WIDTH - filled)} {hours:g}/{target}h`"


def topic_bar(topic: str) -> str:
    plan = plan_file(topic)
    target = int(re.search(r"-(\d+)h\.md$", plan.name).group(1))
    return bar(hours_done(plan.read_text(encoding="utf-8")), target)


def write(topic: str) -> list[Path]:
    """Thay thanh cũ bằng thanh mới ở dòng chủ đề trong README.md và dòng 'Tiến độ' của file lộ trình."""
    new, plan, changed = topic_bar(topic), plan_file(topic), []
    for path, marker in ((REPO / "README.md", f"learning/{plan.name}"), (plan, "**Tiến độ:**")):
        text = path.read_text(encoding="utf-8")
        lines = [BAR_RE.sub(new, l) if marker in l else l for l in text.splitlines(keepends=True)]
        if "".join(lines) != text:
            path.write_text("".join(lines), encoding="utf-8")
            changed.append(path)
    return changed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("topic", nargs="?")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    topic = args.topic or active_topic((LEARNING / "README.md").read_text(encoding="utf-8"))
    if args.write:
        for p in write(topic):
            print(f"cập nhật {p.relative_to(REPO)}")
    print(f"Tiến độ {topic}: {topic_bar(topic).strip('`')}")


if __name__ == "__main__":
    main()
