import importlib.util
from datetime import date
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "flashcard_email.py"
spec = importlib.util.spec_from_file_location("flashcard_email", SCRIPT)
fe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fe)

CARDS = fe.parse_deck(fe.DECK.read_text(encoding="utf-8"))
DAY = date(2026, 11, 3)


def test_deck_parses_with_every_field():
    assert len(CARDS) >= 81
    assert not [(c["id"], f) for c in CARDS for f in fe.FIELDS if not c[f]]
    assert len({c["id"] for c in CARDS}) == len(CARDS)


def test_lesson_is_smallest_session_after_hoc_o():
    assert fe.lesson_of("docs · Học ở: Buổi 16, 21") == 16
    assert fe.lesson_of("x · Học ở: retro buổi 56; chủ đề sau") == 56
    assert fe.lesson_of("x · Học ở: tham khảo (ngoài lab)") == fe.LAST_LESSON


def test_progress_reads_log_and_next_session():
    text = "> **Buổi kế: 3** — mở file X\n\n## Log\n\n| Buổi | Ngày | Giờ | Pass? | Gap |\n|---|---|---|---|---|\n| 0 | d | 0 | ✅ | |\n| 1 | d | 0.75 | ✅ | |\n| 2·mini | d | 1 | — | đang dở |\n\n## Retro\n"
    done, next_line = fe.read_progress(text)
    assert done == 1
    assert next_line.startswith("Buổi kế: 3")


def test_nothing_learned_picks_no_cards():
    assert fe.pick(CARDS, DAY, done=0) == []


def test_last_activity_reads_log_dates_including_mini():
    text = "## Log\n\n| Buổi | Ngày | Giờ | Pass? | Gap |\n|---|---|---|---|---|\n| 0 | 2026-10-27 | 0 | ✅ | |\n| 1·mini | 2026-11-02 | 0.25 | — | |\n\n## Retro\n"
    assert fe.last_activity(text) == date(2026, 11, 2)
    assert fe.last_activity("## Log\n\n## Retro") is None


def test_stall_reminder_after_3_days_then_every_3_days():
    last = date(2026, 10, 27)
    assert all(fe.stall_reminder_due(date(2026, 10, d), last) is None for d in range(27, 31))  # ≤ 3 ngày
    assert fe.stall_reminder_due(date(2026, 10, 31), last) is True     # ngày thứ 4: nhắc
    assert fe.stall_reminder_due(date(2026, 11, 1), last) is False
    assert fe.stall_reminder_due(date(2026, 11, 3), last) is True      # 3 ngày sau: nhắc lại


def test_stall_email_is_one_line_without_blame():
    out = fe.render_stall("Buổi kế: 3 — mở file X → mục tiêu Y")
    assert out["send"] and out["cards"] == []
    assert "\n" not in out["text"] and "`hoc`" in out["text"]
    assert out["text"].startswith("Buổi kế: 3 (~15 phút)")
    assert "ngày" not in out["text"]


def test_only_learned_cards_with_one_recent():
    for done in (1, 6, 25, 56):
        chosen = fe.pick(CARDS, DAY, done)
        assert 1 <= len(chosen) <= fe.PER_DAY
        assert len({c["id"] for c in chosen}) == len(chosen)
        assert all(c["lesson"] <= done for c in chosen)
        assert chosen[0]["lesson"] >= min(max(done - 1, 1), max(c["lesson"] for c in CARDS if c["lesson"] <= done))


def test_answers_come_after_all_questions():
    out = fe.render(fe.pick(CARDS, DAY, 25), DAY)
    html, text = out["html"], out["text"]
    assert html.index("② Đáp án") < html.index("✅ Đáp")
    assert text.index("② ĐÁP ÁN") < text.index("Đáp:")


QUOTES = fe.parse_quotes(fe.QUOTES.read_text(encoding="utf-8"))


def test_quotes_parse_with_source_and_verification():
    assert len(QUOTES) >= 10
    assert not [(q["id"], f) for q in QUOTES for f in ("Dịch", "Tác giả", "Ý cho mình") if not q[f]]
    sources = [l for l in fe.QUOTES.read_text(encoding="utf-8").splitlines() if l.startswith("**Nguồn:**")]
    assert len(sources) == len(QUOTES)
    assert all("✅" in l or "⚠️" in l for l in sources)


def test_quote_rotates_and_leads_card_email():
    assert fe.pick_quote(QUOTES, DAY) != fe.pick_quote(QUOTES, date(2026, 11, 4))
    q = fe.pick_quote(QUOTES, DAY)
    out = fe.render(fe.pick(CARDS, DAY, 25), DAY, q)
    assert out["text"].startswith("💬") and out["html"].index("💬") < out["html"].index("</p>")
