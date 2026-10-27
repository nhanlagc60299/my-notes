"""Sổ ôn tập: mỗi buổi đã có trong Log (trừ buổi 0 intake) phải có file notebook/NN-*.md."""
import re
from pathlib import Path

TOPIC = Path(__file__).resolve().parents[2]
NOTEBOOK = TOPIC / "notebook"
PLAN = next((TOPIC.parent.parent / "learning").glob("ai-agents-*h.md"))


def logged_sessions(plan_text: str) -> set[int]:
    log = plan_text.split("## Log", 1)[-1].split("\n## ", 1)[0]
    return {int(m.group(1)) for m in re.finditer(r"^\|\s*(\d+)(?:·mini)?\s*\|\s*\d{4}-\d{2}-\d{2}", log, flags=re.M)} - {0}


def test_logged_sessions_parses_mini_rows():
    text = "## Log\n| 0 | 2026-10-27 | 0 | ✅ | |\n| 1·mini | 2026-10-28 | 0.25 | — | |\n| 2 | 2026-10-30 | 1.5 | ✅ | |\n"
    assert logged_sessions(text) == {1, 2}


def test_every_logged_session_has_a_notebook_listed_in_index():
    index = (NOTEBOOK / "README.md").read_text(encoding="utf-8")
    for n in logged_sessions(PLAN.read_text(encoding="utf-8")):
        files = sorted(NOTEBOOK.glob(f"{n:02d}-*.md"))
        assert files, f"buổi {n} đã log nhưng chưa có notebook/{n:02d}-<ten>.md"
        assert files[0].name in index, f"{files[0].name} chưa có trong bảng notebook/README.md"


def test_every_question_hides_its_answer():
    """Đáp án phải nằm trong <details> để ôn bằng cách tự nhớ lại, không phải đọc lại."""
    for f in NOTEBOOK.glob("[0-9][0-9]-*.md"):
        text = f.read_text(encoding="utf-8")
        questions = re.findall(r"^### \d+\. ", text, flags=re.M)
        assert questions, f"{f.name} không có câu hỏi nào"
        assert text.count("<details>") >= len(questions), f"{f.name}: có câu chưa giấu đáp án trong <details>"
        assert text.count("**Tôi đã trả lời:**") >= len(questions), f"{f.name}: thiếu câu trả lời của người học"
