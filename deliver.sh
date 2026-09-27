#!/usr/bin/env bash
# After Disco Stu files Hashish: shoot the cover + centerfold, print the issue, ring the bell.
set -u
D="$HOME/.hermes/garden/hashish"; PY="$HOME/.hermes/hermes-agent/venv/bin/python"; M=$(TZ=America/New_York date +%Y-%m)
F="$D/drafts/$M.json"; [ -f "$F" ] || { echo "no Hashish draft for $M"; exit 0; }
cd "$D" && "$PY" build_hashish.py "$F" || exit 1
MISS=$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1]))["pinup"]["title"])' "$F" 2>/dev/null)
"$PY" "$HOME/.hermes/garden/newsstand/notify.py" "💋 Hashish is on the rack" "This month's centerfold: ${MISS:-a Garden machine}" "/hashish/"
