#!/usr/bin/env bash
# Spec validator for kb-infra. Checks the source only; the live systems it
# materializes into are out of scope by design (see docs/adr/0001).
set -uo pipefail

fail=0
err() { printf 'FAIL: %s\n' "$*"; fail=1; }

TMP_BROKEN=$(mktemp)
trap 'rm -f "$TMP_BROKEN"' EXIT

self=':!scripts/check.sh'

# 1. No machine-specific absolute paths in committed files.
if git grep -nI -e '/Users/' -e '/home/' -- "$self" >/dev/null 2>&1; then
  echo "Absolute home paths in committed files:"
  git grep -nI -e '/Users/' -e '/home/' -- "$self"
  fail=1
fi

# 2. No retired terms (catch renames regressing).
for pat in '/recall' '/remember' 'Eval Pulse' 'Tuning Audit' 'Advancement Pulse'; do
  if git grep -nI -e "$pat" -- "$self" >/dev/null 2>&1; then
    echo "Retired term '$pat':"
    git grep -nI -e "$pat" -- "$self"
    fail=1
  fi
done

# 3. No personal project codenames leaking into the generic spec.
for word in AnyPINN Ginevra Orray Scry; do
  if git grep -nwI -e "$word" -- "$self" >/dev/null 2>&1; then
    echo "Personal codename '$word':"
    git grep -nwI -e "$word" -- "$self"
    fail=1
  fi
done

# 4. Each skill has name + description frontmatter.
for f in skills/*/SKILL.md; do
  [ -f "$f" ] || continue
  head -6 "$f" | grep -q '^name:' || err "$f missing 'name:' frontmatter"
  head -6 "$f" | grep -q '^description:' || err "$f missing 'description:' frontmatter"
done

# 5. Preamble exists and every automation references it.
if [ ! -f docs/automations/_preamble.md ]; then
  err "docs/automations/_preamble.md is missing"
else
  for f in docs/automations/*.md; do
    [ "$f" = "docs/automations/_preamble.md" ] && continue
    grep -q '_preamble' "$f" || err "$f does not reference the shared preamble"
  done
fi

# 6. Internal markdown links resolve.
while IFS= read -r md; do
  dir=$(dirname "$md")
  # extract ](target) from links and images
  grep -oE '\]\([^)#]+' "$md" 2>/dev/null | sed -E 's/^\]\(//' | while IFS= read -r target; do
    case "$target" in
      http*|mailto:*|'{{'*|'') continue ;;
    esac
    resolved="$dir/$target"
    if [ ! -e "$resolved" ]; then
      printf 'FAIL: broken link in %s -> %s\n' "$md" "$target"
      echo brokenlink >> "$TMP_BROKEN"
    fi
  done
done < <(git ls-files '*.md')

if [ -s "$TMP_BROKEN" ]; then fail=1; fi

# 7. Job-hunt advancement stays sink-agnostic while declaring the concrete
# capabilities setup must bind into a self-contained materialization.
ADVANCE_SPEC='docs/automations/job-hunt-advance-audit.md'
DECLARED_CAPABILITIES=$(sed -n 's/^- Sink capabilities: //p' "$ADVANCE_SPEC" | grep -oE '`[a-z0-9-]+`' | tr -d '`')
if [ -z "$DECLARED_CAPABILITIES" ]; then
  err "$ADVANCE_SPEC declares no sink capabilities"
fi
while IFS= read -r capability; do
  [ -n "$capability" ] || continue
  grep -q "${capability}" "$ADVANCE_SPEC" || err "$ADVANCE_SPEC missing sink capability '${capability}'"
  grep -q "${capability}" docs/automations/_preamble.md || err "_preamble.md missing sink capability '${capability}'"
  grep -q "${capability}" local/bindings.example.yml || err "bindings.example.yml missing sink capability '${capability}'"
done <<< "$DECLARED_CAPABILITIES"
grep -q '## Sink capabilities' skills/setup-kb-infra/SKILL.md || err 'setup skill does not compose declared sink capabilities'
if grep -Eq 'candidacy-select\.mjs|modes/next\.md|career-ops next' "$ADVANCE_SPEC"; then
  err "$ADVANCE_SPEC hardcodes one career-system implementation instead of bound capabilities"
fi
grep -q 'automation body explicitly classifies a narrow in-mandate write' docs/automations/_preamble.md || \
  err '_preamble.md approval rule does not recognize explicitly authorized safe internal writes'

if [ "$fail" -ne 0 ]; then
  echo "spec check: FAILED"
  exit 1
fi
echo "spec check: OK"
