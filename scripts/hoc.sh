# hoc — vào thẳng buổi học: cd lab, bật .venv, chạy test, in "Buổi kế" + tiến độ.
#
# Dùng `source` để giữ cd và venv trong shell hiện tại. Thêm vào ~/.zshrc hoặc ~/.bashrc:
#     hoc() { cd ~/path/to/my-notes && source scripts/hoc.sh "$@"; }
# Rồi gõ: hoc            (chủ đề 🟢 trong learning/README.md)
#         hoc ai-agents  (chủ đề cụ thể)
# Chạy kiểu `bash scripts/hoc.sh` cũng được, nhưng shell của bạn không giữ cd/venv.
# Viết cho bash và zsh; không dùng `exit` vì file được source.

_hoc() {
  local repo topic plan lab py rc out
  repo=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "hoc: hãy chạy trong repo my-notes"; return 1; }
  topic=${1:-$(grep '🟢' "$repo/learning/README.md" | grep -oE '\([a-z0-9-]+-[0-9]+h\.md\)' | head -n 1 | sed -E 's/^\(//; s/-[0-9]+h\.md\)$//')}
  plan=$(find "$repo/learning" -maxdepth 1 -name "$topic-*h.md" 2>/dev/null | head -n 1)
  lab="$repo/topics/$topic/lab"
  if [ -z "$topic" ] || [ -z "$plan" ] || [ ! -d "$lab" ]; then
    echo "hoc: không tìm thấy chủ đề '$topic' (cần learning/<topic>-<N>h.md và topics/<topic>/lab)"; return 1
  fi
  cd "$lab" || return 1

  if [ -f .venv/bin/activate ]; then
    . .venv/bin/activate
  elif [ -z "$VIRTUAL_ENV" ]; then
    echo "Chưa có .venv. Setup 1 lần:"
    echo "  python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt"
    echo
  fi
  py=python3; [ -n "$VIRTUAL_ENV" ] && py=python

  echo "▶ pytest -q ($topic)"
  $py -m pytest -q 2>&1 | tail -n 3
  echo

  out=$($py -m pytest -q -m next 2>&1); rc=$?
  if [ "$rc" -ne 5 ]; then
    echo "▶ Việc hôm nay: test đỏ có chủ đích (pytest -m next)"
    printf '%s\n' "$out" | grep -E '^(FAILED|PASSED|ERROR)|passed|failed' | head -n 5
    echo
  fi

  grep -E '^> \*\*(Buổi kế|Bước tiếp theo)' "$plan" | sed -E 's/^> //; s/\*\*//g; s/\[([^]]*)\]\([^)]*\)/\1/g'
  python3 "$repo/scripts/progress.py" "$topic"
  echo 'Có 10–15 phút? Làm phiên mini. Mở Claude ở đây và gõ "học tiếp".'
}
_hoc "$@"
unset -f _hoc
