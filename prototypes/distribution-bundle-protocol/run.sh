#!/usr/bin/env bash
set -euo pipefail

prototype_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

if [[ ${1:-} == --all ]]; then
  exec python3 "$prototype_dir/model.py" --all
fi

bold=$'\033[1m'
dim=$'\033[2m'
reset=$'\033[0m'
selected=allowlist

render() {
  clear 2>/dev/null || printf '\033[2J\033[H'
  printf '%sDistribution Bundle protocol prototype%s\n\n' "$bold" "$reset"
  printf '%sQuestion%s\n' "$bold" "$reset"
  printf '%sCan one level-triggered full rebuild safely handle every publication edge case?%s\n\n' "$dim" "$reset"
  python3 "$prototype_dir/model.py" "$selected"
  printf '\n%sActions%s\n' "$bold" "$reset"
  printf '%s[a]%s allowlist  %s[c]%s concurrency  %s[r]%s removal  %s[n]%s collision\n' "$bold" "$reset" "$bold" "$reset" "$bold" "$reset" "$bold" "$reset"
  printf '%s[u]%s unauthorized  %s[m]%s mutable  %s[b]%s rollback  %s[o]%s no-op  %s[q]%s quit\n' "$bold" "$reset" "$bold" "$reset" "$bold" "$reset" "$bold" "$reset" "$bold" "$reset"
}

while true; do
  render
  IFS= read -r -n 1 key
  case "$key" in
    a) selected=allowlist ;;
    c) selected=concurrent ;;
    r) selected=removal ;;
    n) selected=collision ;;
    u) selected=unauthorized ;;
    m) selected=mutable ;;
    b) selected=rollback ;;
    o) selected=noop ;;
    q) break ;;
  esac
done

