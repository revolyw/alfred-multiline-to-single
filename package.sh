#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/Multiline to Single.alfredworkflow"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

required=(
  info.plist
  filter.py
  LICENSE
  README.md
)

for f in "${required[@]}"; do
  if [[ ! -f "$ROOT/$f" ]]; then
    echo "missing required file: $f" >&2
    exit 1
  fi
  cp "$ROOT/$f" "$STAGE/"
done

# Optional extras packed when present
for f in README.en.md CHANGELOG.md; do
  if [[ -f "$ROOT/$f" ]]; then
    cp "$ROOT/$f" "$STAGE/"
  fi
done

chmod +x "$STAGE/filter.py"

rm -f "$OUT"
(
  cd "$STAGE"
  zip -q -r "$OUT" .
)

echo "Packed: $OUT"
unzip -l "$OUT"
