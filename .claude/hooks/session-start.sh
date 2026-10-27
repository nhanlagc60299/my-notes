#!/bin/bash
# SessionStart: (1) trên Claude Code cloud thì cài dependency của lab vào .venv,
# (2) luôn in trạng thái học để session mới biết ngay phải dạy gì (stdout vào ngữ cảnh).
set -euo pipefail
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
  for req in topics/*/lab/requirements.txt; do
    lab=$(dirname "$req")
    [ -x "$lab/.venv/bin/python" ] || python3 -m venv "$lab/.venv" >&2
    "$lab/.venv/bin/python" -m pip install -q --disable-pip-version-check -r "$req" >&2
  done
  topic=$(python3 -c 'import sys; sys.path.insert(0, "scripts"); from progress import active_topic, LEARNING; print(active_topic((LEARNING / "README.md").read_text(encoding="utf-8")))')
  if [ -n "${CLAUDE_ENV_FILE:-}" ] && [ -d "topics/$topic/lab/.venv" ]; then
    echo "export VIRTUAL_ENV=\"$PWD/topics/$topic/lab/.venv\"" >> "$CLAUDE_ENV_FILE"
    echo "export PATH=\"$PWD/topics/$topic/lab/.venv/bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
  fi
  echo "(Cloud session: không có Ollama. Test chạy offline bằng FakeLLM; bước cần LLM_BACKEND=ollama thì người học chạy trên máy mình rồi dán output vào chat.)"
fi

python3 scripts/status.py || echo "Không đọc được trạng thái học: chạy python3 scripts/status.py"
