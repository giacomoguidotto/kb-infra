#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
installer="$repo_root/skills/public/setup-knowledge-system/scripts/reconcile-interface.sh"
fixture=$(mktemp -d)
trap 'rm -rf "$fixture"' EXIT

harness_root="$fixture/harness/skills"
bindings="$fixture/local/bindings.yml"
runtime_state="$fixture/harness/runtime/kb-reconcile.yml"
mkdir -p "$(dirname "$bindings")" "$(dirname "$runtime_state")"
printf 'provider:\n  name: example\n  connector: example-connector\ncustom: keep-me\n' > "$bindings"
printf 'last_completed_at: "2026-07-20T10:00:00Z"\nhistory: keep-me\n' > "$runtime_state"

bindings_before=$(shasum -a 256 "$bindings" | cut -d' ' -f1)
runtime_before=$(shasum -a 256 "$runtime_state" | cut -d' ' -f1)

first=$(bash "$installer" reconcile "$harness_root")
case "$first" in
  *'state=converged writes=1'*) ;;
  *) printf 'FAIL: first reconcile did not install the interface: %s\n' "$first" >&2; exit 1 ;;
esac

tree_before=$(find "$harness_root" -type f -exec shasum -a 256 {} \; | LC_ALL=C sort)
second=$(bash "$installer" reconcile "$harness_root")
tree_after=$(find "$harness_root" -type f -exec shasum -a 256 {} \; | LC_ALL=C sort)

case "$second" in
  *'state=converged writes=0'*) ;;
  *) printf 'FAIL: second reconcile was not a zero-write no-op: %s\n' "$second" >&2; exit 1 ;;
esac
[ "$tree_before" = "$tree_after" ] || { printf 'FAIL: second reconcile changed installed content\n' >&2; exit 1; }
[ "$bindings_before" = "$(shasum -a 256 "$bindings" | cut -d' ' -f1)" ] || { printf 'FAIL: bindings changed\n' >&2; exit 1; }
[ "$runtime_before" = "$(shasum -a 256 "$runtime_state" | cut -d' ' -f1)" ] || { printf 'FAIL: runtime history changed\n' >&2; exit 1; }
[ ! -e "$fixture/local/installed.yml" ] || { printf 'FAIL: setup receipt created\n' >&2; exit 1; }
[ ! -e "$fixture/local/automations" ] || { printf 'FAIL: prompt snapshot created\n' >&2; exit 1; }

printf 'setup reconcile idempotency: OK\n'
