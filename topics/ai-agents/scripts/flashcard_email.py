"""Render email flashcard hằng ngày từ topics/ai-agents/flashcards.md.

    python topics/ai-agents/scripts/flashcard_email.py              # hôm nay (Asia/Ho_Chi_Minh)
    python topics/ai-agents/scripts/flashcard_email.py --date 2026-10-28 --html-out /tmp/preview.html
    python topics/ai-agents/scripts/flashcard_email.py --done 10    # giả lập đã xong buổi 10 (bỏ qua kiểm tra chững)

In ra JSON {send, subject, html, text, cards, reason}. Scheduled task chạy script này;
`send` = true thì gửi `html` (kèm `text` làm bản plain-text) qua Gmail, không tự soạn lại
nội dung; `send` = false thì không gửi gì.

Nguyên tắc (retrieval practice + spacing):
- Chỉ gửi thẻ của buổi **đã học** (đọc bảng Log trong learning/ai-agents-*.md).
  Buổi của thẻ = số buổi nhỏ nhất trong "Học ở:" ở trường Nguồn.
- Mỗi ngày: 1 thẻ của buổi gần nhất + 2 thẻ cũ để ôn (xoay vòng theo ngày).
- Câu hỏi ở đầu email, toàn bộ nội dung + đáp án ở cuối: tự nhớ lại trước khi xem.
- Nhắc khi chững, không nhắc hằng ngày: nếu dòng cuối của Log cũ hơn 3 ngày thì
  chỉ gửi 1 dòng "Buổi kế … (~15 phút) — gõ `hoc`", lặp lại mỗi 3 ngày (giống
  `for: 3d` + `repeat_interval: 3d` của alert). Đây là thiết kế theo kiểu cảnh báo
  SRE, không có nghiên cứu riêng kiểm chứng.
- Không chững nhưng chưa có thẻ nào để ôn → không gửi gì.
- Đầu email là 1 câu truyền cảm hứng trong quotes.md (xoay vòng theo ngày).
"""
from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TOPIC = Path(__file__).resolve().parent.parent
DECK = TOPIC / "flashcards.md"
QUOTES = TOPIC / "quotes.md"
LEARNING_DIR = TOPIC.parent.parent / "learning"
START = date(2026, 10, 28)
PER_DAY = 3
STALL_DAYS = 3    # Log im lặng quá số ngày này thì coi là chững
REPEAT_DAYS = 3   # đang chững thì nhắc lại sau mỗi chừng này ngày
LAST_LESSON = 56  # thẻ không gắn buổi cụ thể (tham khảo, chủ đề sau) chỉ gửi khi xong lộ trình
FIELDS = ["Cấp", "Nói đơn giản", "Ví dụ đời thường", "Trong agent email", "Liên tưởng SRE", "Nhớ", "Tự kiểm tra", "Đáp", "Nguồn"]
REPO_URL = "https://github.com/nhanlagc60299/my-notes/blob/main/topics/ai-agents/flashcards.md"
NOTEBOOK_URL = "https://github.com/nhanlagc60299/my-notes/tree/main/topics/ai-agents/notebook"
FONT = "font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;max-width:680px;margin:auto;color:#1f2328;line-height:1.55;font-size:15px"


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
        card["lesson"] = lesson_of(card["Nguồn"])
        cards.append(card)
    return cards


def lesson_of(source: str) -> int:
    """Buổi nhỏ nhất trong phần 'Học ở:' của Nguồn; không có số buổi thì coi là cuối lộ trình."""
    _, _, where = source.partition("Học ở:")
    nums = [int(n) for n in re.findall(r"(?i)buổi\s*(\d+)", where)]
    return min(nums) if nums else LAST_LESSON


def read_progress(learning_text: str) -> tuple[int, str]:
    """(buổi lớn nhất đã pass trong bảng Log, dòng 'Buổi kế')."""
    log = learning_text.split("## Log", 1)[-1].split("\n## ", 1)[0]
    done = 0
    for row in log.splitlines():
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        m = re.match(r"(\d+)", cells[0]) if cells else None
        if m and len(cells) >= 4 and "✅" in cells[3]:
            done = max(done, int(m.group(1)))
    nm = re.search(r"^> \*\*Buổi kế:\s*(.+?)\*\*\s*(.*)$", learning_text, flags=re.M)
    next_line = f"Buổi kế: {nm.group(1).strip()} {nm.group(2).strip()}".strip() if nm else "Buổi kế: xem learning/"
    return done, re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", next_line)


def last_activity(learning_text: str) -> date | None:
    """Ngày mới nhất trong bảng Log (cả dòng phiên mini)."""
    log = learning_text.split("## Log", 1)[-1].split("\n## ", 1)[0]
    days = [date.fromisoformat(d) for d in re.findall(r"^\|[^|\n]*\|\s*(\d{4}-\d{2}-\d{2})\s*\|", log, flags=re.M)]
    return max(days) if days else None


def stall_reminder_due(day: date, last: date | None) -> bool | None:
    """None = chưa chững; True = chững và hôm nay đến lượt nhắc; False = chững nhưng chưa tới lượt nhắc lại."""
    idle = (day - last).days if last else 0
    if idle <= STALL_DAYS:
        return None
    return (idle - STALL_DAYS - 1) % REPEAT_DAYS == 0


def parse_quotes(text: str) -> list[dict]:
    quotes = []
    for block in re.split(r"^### ", text, flags=re.M)[1:]:
        header, _, body = block.partition("\n")
        m = re.match(r"(Q-\d+)\s*·\s*(.+)", header.strip())
        qm = re.search(r'^>\s*"(.+)"\s*$', body, flags=re.M)
        if not (m and qm):
            continue
        q = {"id": m.group(1), "group": m.group(2).strip(), "quote": qm.group(1)}
        for field in ("Dịch", "Tác giả", "Ý cho mình"):
            fm = re.search(rf"^\*\*{field}:\*\*\s*(.+)$", body, flags=re.M)
            q[field] = fm.group(1).strip() if fm else ""
        quotes.append(q)
    return quotes


def pick_quote(quotes: list[dict], day: date) -> dict | None:
    return quotes[max((day - START).days, 0) % len(quotes)] if quotes else None


def quote_block(q: dict | None) -> tuple[str, str]:
    """(html, text) của khung câu truyền cảm hứng; rỗng nếu không có câu."""
    if not q:
        return "", ""
    h = ('<div style="border-left:4px solid #8250df;background:#fbefff;padding:12px 16px;border-radius:6px;margin:0 0 18px">'
         f'<div style="font-size:12px;color:#57606a">💬 {inline_html(q["group"])}</div>'
         f'<p style="margin:4px 0;font-size:16px"><i>“{inline_html(q["quote"])}”</i></p>'
         f'<p style="margin:4px 0">{inline_html(q["Dịch"])}</p>'
         f'<p style="margin:4px 0;font-size:13px;color:#57606a">— {inline_html(q["Tác giả"])}</p>'
         f'<p style="margin:8px 0 0;font-size:14px">👉 {inline_html(q["Ý cho mình"])}</p></div>')
    t = f'💬 "{q["quote"]}"\n{q["Dịch"]}\n— {q["Tác giả"]}\n👉 {inline_text(q["Ý cho mình"])}\n'
    return h, t


def pick(cards: list[dict], day: date, done: int) -> list[dict]:
    """1 thẻ của buổi gần nhất + 2 thẻ cũ để ôn, chỉ trong các thẻ đã học tới."""
    eligible = [c for c in cards if c["lesson"] <= done]
    if not eligible:
        return []
    d = max((day - START).days, 0)
    recent = [c for c in eligible if c["lesson"] >= max(done - 1, 1)] or \
             [c for c in eligible if c["lesson"] == max(x["lesson"] for x in eligible)]
    older = [c for c in eligible if c not in recent]
    chosen = [recent[d % len(recent)]]
    for i in range(2):
        pool = older or recent
        for k in range(len(pool)):
            cand = pool[(2 * d + i + k) % len(pool)]
            if cand not in chosen:
                chosen.append(cand)
                break
    return chosen[:PER_DAY]


def inline_html(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r'<code style="background:#f1f3f5;padding:1px 4px;border-radius:3px;font-size:13px">\1</code>', s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)


def inline_text(s: str) -> str:
    return s.replace("**", "")


def short(title: str) -> str:
    return title.split(" — ")[0]


def skip(reason: str) -> dict:
    return {"send": False, "reason": reason, "subject": "", "html": "", "text": "", "cards": []}


def render_stall(next_line: str) -> dict:
    """Đúng một dòng: không trách, không đếm số ngày đã nghỉ, chỉ chỉ ra bước nhỏ nhất."""
    head = next_line.split("—")[0].strip()
    line = f"{head} (~15 phút) — gõ `hoc`, rồi \"học tiếp\"."
    return {"send": True, "reason": "stall", "subject": f"⏰ AI Agents · {head} (~15 phút)",
            "html": f'<div style="{FONT}"><p style="margin:10px 0">{inline_html(line)}</p></div>',
            "text": inline_text(line), "cards": []}


def render(cards: list[dict], day: date, quote: dict | None = None) -> dict:
    ids = ", ".join(c["id"] for c in cards)
    subject = f"🧠 AI Agents · {day:%d/%m} · {' · '.join(short(c['title']) for c in cards)}"
    labels = [("Nói đơn giản", "💡"), ("Ví dụ đời thường", "🏠"), ("Trong agent email", "📧"), ("Liên tưởng SRE", "🛠️"), ("Nhớ", "📌")]

    qh, qt = quote_block(quote)
    parts = [f'<div style="{FONT}">', qh,
             f'<p style="color:#57606a;margin:0 0 12px">{len(cards)} thẻ hôm nay ({ids}): 1 thẻ buổi gần nhất + thẻ cũ để ôn.</p>',
             '<h2 style="font-size:18px;margin:0 0 8px">① Tự nhớ lại trước (đừng kéo xuống vội)</h2>',
             '<p style="color:#57606a;margin:0 0 10px">Trả lời trong đầu hoặc ra giấy, rồi mới xem đáp án ở phần ②.</p><ol>']
    text = ([qt] if qt else []) + [f"{len(cards)} thẻ hôm nay ({ids})", "", "① TỰ NHỚ LẠI TRƯỚC (đừng kéo xuống vội)"]
    for i, c in enumerate(cards, 1):
        parts.append(f'<li style="margin:8px 0"><b>{inline_html(short(c["title"]))}</b>: {inline_html(c["Tự kiểm tra"])}</li>')
        text.append(f"{i}. {inline_text(short(c['title']))}: {inline_text(c['Tự kiểm tra'])}")
    parts.append("</ol>")
    parts.append('<div style="height:900px"></div>'
                 '<p style="text-align:center;color:#57606a;border-top:2px dashed #d0d7de;padding-top:12px">▼ ② Đáp án và bài học ▼</p>')
    text += ["", *["."] * 25, "", "② ĐÁP ÁN VÀ BÀI HỌC"]
    for c in cards:
        parts.append('<div style="border:1px solid #d0d7de;border-radius:8px;padding:16px 18px;margin:0 0 18px">')
        parts.append(f'<div style="font-size:12px;color:#57606a">{c["id"]} · Cấp {inline_html(c["Cấp"])}</div>'
                     f'<h3 style="font-size:17px;margin:2px 0 10px">{inline_html(c["title"])}</h3>'
                     f'<p style="margin:6px 0"><b>❓ Tự kiểm tra:</b> {inline_html(c["Tự kiểm tra"])}</p>'
                     f'<p style="margin:6px 0 12px;color:#1a7f37"><b>✅ Đáp:</b> {inline_html(c["Đáp"])}</p>')
        text.append(f"\n===== {c['id']} · {inline_text(c['title'])} (Cấp {inline_text(c['Cấp'])}) =====")
        text.append(f"Tự kiểm tra: {inline_text(c['Tự kiểm tra'])}\nĐáp: {inline_text(c['Đáp'])}")
        for field, icon in labels:
            if c[field]:
                bg = ' style="background:#fff8c5;padding:8px 10px;border-radius:6px;margin:10px 0"' if field == "Nhớ" else ' style="margin:8px 0"'
                parts.append(f'<p{bg}><b>{icon} {field}:</b> {inline_html(c[field])}</p>')
                text.append(f"{field}: {inline_text(c[field])}")
        parts.append(f'<p style="font-size:12px;color:#57606a;margin:10px 0 0">Nguồn: {inline_html(c["Nguồn"])}</p></div>')
        text.append(f"Nguồn: {inline_text(c['Nguồn'])}")
    footer = f'Cả bộ thẻ: <a href="{REPO_URL}">flashcards.md</a> · Rảnh thì ôn <a href="{NOTEBOOK_URL}">sổ ôn tập</a> (câu ❌ trước) · Học tiếp (phiên mini 10–15 phút cũng tính): mở Claude trong repo my-notes và gõ "học tiếp".'
    parts.append(f'<p style="font-size:13px;color:#57606a">{footer}</p></div>')
    text.append(f"\nCả bộ thẻ: {REPO_URL}\nSổ ôn tập (câu ❌ trước): {NOTEBOOK_URL}\nHọc tiếp (phiên mini 10–15 phút cũng tính): mở Claude trong repo my-notes và gõ \"học tiếp\".")
    return {"send": True, "reason": "cards", "subject": subject, "html": "\n".join(parts), "text": "\n".join(text), "cards": [c["id"] for c in cards]}


def build(day: date, done: int | None = None) -> dict:
    cards = parse_deck(DECK.read_text(encoding="utf-8"))
    learning = sorted(LEARNING_DIR.glob("ai-agents-*.md"))
    text = learning[0].read_text(encoding="utf-8") if learning else ""
    progress_done, next_line = read_progress(text) if text else (0, "Buổi kế: xem learning/")
    if done is None:  # --done là giả lập để xem trước, nên bỏ qua kiểm tra chững
        due = stall_reminder_due(day, last_activity(text))
        if due is not None:
            return render_stall(next_line) if due else skip("đang chững, chưa tới lượt nhắc lại")
    chosen = pick(cards, day, progress_done if done is None else done)
    if not chosen:
        return skip("chưa xong buổi nào có thẻ")
    quote = pick_quote(parse_quotes(QUOTES.read_text(encoding="utf-8")) if QUOTES.exists() else [], day)
    return render(chosen, day, quote)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD (mặc định: hôm nay giờ Việt Nam)")
    ap.add_argument("--done", type=int, help="giả lập số buổi đã xong (mặc định: đọc từ bảng Log)")
    ap.add_argument("--html-out", help="ghi HTML ra file để xem trước")
    args = ap.parse_args()
    day = date.fromisoformat(args.date) if args.date else datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).date()
    out = build(day, args.done)
    if args.html_out and out["send"]:
        Path(args.html_out).write_text(out["html"], encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
