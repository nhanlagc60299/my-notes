"""Render email flashcard hằng ngày từ topics/ai-agents/flashcards.md.

    python topics/ai-agents/scripts/flashcard_email.py              # hôm nay (Asia/Ho_Chi_Minh)
    python topics/ai-agents/scripts/flashcard_email.py --date 2026-10-28 --html-out /tmp/preview.html

In ra JSON {subject, html, text, cards}. Scheduled task chạy script này rồi gửi
`html` (kèm `text` làm bản plain-text) qua Gmail — không tự soạn lại nội dung.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

DECK = Path(__file__).resolve().parent.parent / "flashcards.md"
START = date(2026, 10, 28)
PER_DAY = 3
FIELDS = ["Cấp", "Nói đơn giản", "Ví dụ đời thường", "Trong agent email", "Liên tưởng SRE", "Nhớ", "Tự kiểm tra", "Đáp", "Nguồn"]
REPO_URL = "https://github.com/nhanlagc60299/my-notes/blob/main/topics/ai-agents/flashcards.md"


def parse_deck(text: str) -> list[dict]:
    cards = []
    for block in re.split(r"^### ", text, flags=re.M)[1:]:
        header, _, body = block.partition("\n")
        m = re.match(r"(FC-\d+)\s*·\s*(.+)", header.strip())
        if not m:
            continue
        card = {"id": m.group(1), "title": m.group(2).strip()}
        for field in FIELDS:
            fm = re.search(rf"^\*\*{re.escape(field)}:\*\*\s*(.+)$", body, flags=re.M)
            card[field] = fm.group(1).strip() if fm else ""
        cards.append(card)
    return cards


def pick(cards: list[dict], day: date) -> tuple[list[dict], int]:
    d = max((day - START).days, 0)
    n = len(cards)
    chosen = [cards[(PER_DAY * d + i) % n] for i in range(PER_DAY)]
    return chosen, (PER_DAY * d) // n + 1


def inline_html(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r'<code style="background:#f1f3f5;padding:1px 4px;border-radius:3px;font-size:13px">\1</code>', s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)


def inline_text(s: str) -> str:
    return s.replace("**", "")


def render(cards: list[dict], day: date, round_no: int) -> dict:
    ids = ", ".join(c["id"] for c in cards)
    subject = f"🧠 AI Agents · {day:%d/%m} · {' · '.join(c['title'].split(' — ')[0] for c in cards)}"
    labels = [("Nói đơn giản", "💡"), ("Ví dụ đời thường", "🏠"), ("Trong agent email", "📧"), ("Liên tưởng SRE", "🛠️"), ("Nhớ", "📌")]

    parts = [f'<div style="font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;max-width:680px;margin:auto;color:#1f2328;line-height:1.55;font-size:15px">',
             f'<p style="color:#57606a;margin:0 0 16px">3 khái niệm hôm nay ({ids}) · vòng {round_no}. Mỗi thẻ đọc khoảng 2 phút.</p>']
    text = [f"3 khái niệm hôm nay ({ids}) · vòng {round_no}\n"]
    for c in cards:
        parts.append('<div style="border:1px solid #d0d7de;border-radius:8px;padding:16px 18px;margin:0 0 18px">')
        parts.append(f'<div style="font-size:12px;color:#57606a">{c["id"]} · Cấp {inline_html(c["Cấp"])}</div>'
                     f'<h2 style="font-size:18px;margin:2px 0 12px">{inline_html(c["title"])}</h2>')
        text.append(f"\n===== {c['id']} · {inline_text(c['title'])} (Cấp {inline_text(c['Cấp'])}) =====")
        for field, icon in labels:
            if c[field]:
                bg = ' style="background:#fff8c5;padding:8px 10px;border-radius:6px;margin:10px 0"' if field == "Nhớ" else ' style="margin:8px 0"'
                parts.append(f'<p{bg}><b>{icon} {field}:</b> {inline_html(c[field])}</p>')
                text.append(f"{field}: {inline_text(c[field])}")
        parts.append('<div style="border-top:1px dashed #d0d7de;margin-top:12px;padding-top:10px">'
                     f'<p style="margin:6px 0"><b>❓ Tự kiểm tra:</b> {inline_html(c["Tự kiểm tra"])}</p>'
                     f'<p style="margin:6px 0;color:#1a7f37"><b>✅ Đáp:</b> {inline_html(c["Đáp"])}</p></div>'
                     f'<p style="font-size:12px;color:#57606a;margin:10px 0 0">Nguồn: {inline_html(c["Nguồn"])}</p></div>')
        text.append(f"Tự kiểm tra: {inline_text(c['Tự kiểm tra'])}\nĐáp: {inline_text(c['Đáp'])}\nNguồn: {inline_text(c['Nguồn'])}")
    footer = f'Cả bộ thẻ: <a href="{REPO_URL}">flashcards.md</a> · Học tiếp: mở Claude trong repo my-notes và gõ "học tiếp".'
    parts.append(f'<p style="font-size:13px;color:#57606a">{footer}</p></div>')
    text.append(f"\nCả bộ thẻ: {REPO_URL}\nHọc tiếp: mở Claude trong repo my-notes và gõ \"học tiếp\".")
    return {"subject": subject, "html": "\n".join(parts), "text": "\n".join(text), "cards": [c["id"] for c in cards]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD (mặc định: hôm nay giờ Việt Nam)")
    ap.add_argument("--html-out", help="ghi HTML ra file để xem trước")
    args = ap.parse_args()
    day = date.fromisoformat(args.date) if args.date else datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).date()
    cards = parse_deck(DECK.read_text(encoding="utf-8"))
    chosen, round_no = pick(cards, day)
    out = render(chosen, day, round_no)
    if args.html_out:
        Path(args.html_out).write_text(out["html"], encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
