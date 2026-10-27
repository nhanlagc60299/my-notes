import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[4] / "scripts" / "progress.py"
spec = importlib.util.spec_from_file_location("progress", SCRIPT)
pg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pg)


def test_bar_counts_hours_not_days():
    assert pg.bar(0, 40) == "`░░░░░░░░░░ 0/40h`"
    assert pg.bar(6, 20) == "`███░░░░░░░ 6/20h`"
    assert pg.bar(50, 40).startswith("`██████████ ")


def test_hours_read_from_log_including_mini_rows():
    text = "## Log\n\n| Buổi | Ngày | Giờ tích luỹ | Pass? | Gap |\n|---|---|---|---|---|\n| 0 | 2026-10-27 | 0 | ✅ | |\n| 1·mini | 2026-10-28 | 0,25 | — | |\n| 1 | 2026-10-29 | 0.75 | ✅ | |\n\n## Retro\n"
    assert pg.hours_done(text) == 0.75


def test_active_topic_from_queue():
    assert pg.active_topic((pg.LEARNING / "README.md").read_text(encoding="utf-8")) == "ai-agents"


def test_bars_in_readme_and_plan_are_current():
    """Quên chạy `python3 scripts/progress.py --write` ở kết buổi thì test này đỏ."""
    current = pg.topic_bar("ai-agents")
    assert current in (pg.REPO / "README.md").read_text(encoding="utf-8")
    assert current in pg.plan_file("ai-agents").read_text(encoding="utf-8")


def test_status_tells_a_fresh_session_what_to_teach():
    spec2 = importlib.util.spec_from_file_location("status", SCRIPT.parent / "status.py")
    st = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(st)
    out = st.status("ai-agents")
    for must in ("Buổi kế:", "Tiến độ:", "Dòng Log cuối:", "Test `next`", "Câu ❌"):
        assert must in out
