#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'usage: %s check|reconcile <harness-skill-root>\n' "$0" >&2
  exit 64
}

[ "$#" -eq 2 ] || usage
mode=$1
harness_root=$2
case "$mode" in
  check|reconcile) ;;
  *) usage ;;
esac

[ -n "$harness_root" ] || usage
case "$harness_root" in
  /|.|..) printf 'unsafe harness skill root: %s\n' "$harness_root" >&2; exit 65 ;;
esac

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source_tree=$(cd "$script_dir/../resources/knowledge-system-interface/v1" && pwd)
interface_parent="$harness_root/knowledge-system-interface"
target_tree="$interface_parent/v1"

if [ -d "$target_tree" ] && diff -qr "$source_tree" "$target_tree" >/dev/null; then
  printf 'state=converged writes=0 target=%s\n' "$target_tree"
  exit 0
fi

if [ "$mode" = check ]; then
  printf 'state=drifted writes=0 target=%s\n' "$target_tree"
  exit 0
fi

mkdir -p "$interface_parent"
candidate=$(mktemp -d "$interface_parent/.v1-candidate.XXXXXX")
backup=''
cleanup() {
  [ ! -d "$candidate" ] || rm -rf "$candidate"
  if [ -n "$backup" ] && [ -d "$backup" ] && [ ! -e "$target_tree" ]; then
    mv "$backup" "$target_tree"
  fi
}
trap cleanup EXIT

cp -R "$source_tree/." "$candidate/"
if find "$candidate" -name SKILL.md -print -quit | grep -q .; then
  printf 'candidate interface contains SKILL.md\n' >&2
  exit 66
fi
diff -qr "$source_tree" "$candidate" >/dev/null

if [ -e "$target_tree" ]; then
  backup="$interface_parent/.v1-backup.$$"
  [ ! -e "$backup" ] || { printf 'backup path already exists: %s\n' "$backup" >&2; exit 67; }
  mv "$target_tree" "$backup"
fi
mv "$candidate" "$target_tree"
candidate=''
if [ -n "$backup" ]; then
  rm -rf "$backup"
  backup=''
fi
trap - EXIT

printf 'state=converged writes=1 target=%s\n' "$target_tree"
