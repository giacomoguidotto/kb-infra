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

# 8. Every automation declares a provider-agnostic execution profile, and setup has
# a concrete local model binding slot without committing provider model ids.
AUTOMATION_SPECS=(
  docs/automations/knowledge-harvest.md
  docs/automations/social-draft-pulse.md
  docs/automations/portfolio-surface-sweep.md
  docs/automations/job-hunt-evaluate-audit.md
  docs/automations/job-hunt-advance-audit.md
)
MODEL_EXAMPLE=$(sed -n '/^models:/,/^[a-z][a-z_-]*:/p' local/bindings.example.yml)
for spec in "${AUTOMATION_SPECS[@]}"; do
  profile=$(sed -n 's/^- Execution profile: `\([^`]*\)`.*/\1/p' "$spec")
  case "$profile" in
    frontier/medium|frontier/high|frontier/parallel|balanced/medium|balanced/high|efficient/low|efficient/medium) ;;
    '') err "$spec declares no execution profile" ;;
    *) err "$spec declares unsupported execution profile '$profile'" ;;
  esac
  automation=$(basename "$spec" .md)
  grep -q "^  ${automation}:$" <<< "$MODEL_EXAMPLE" || \
    err "bindings.example.yml missing model slot for '${automation}'"
done
grep -q 'reasoning_effort:' local/installed.example.yml || \
  err 'installed.example.yml does not record reasoning effort'
grep -q 'Reconcile the Runtime Model Bindings' skills/setup-kb-infra/SKILL.md || \
  err 'setup skill does not reconcile runtime model bindings'
if git grep -nIE 'gpt-[0-9]|claude-[0-9]|gemini-[0-9]' -- ':!local/*.yml' ':!scripts/check.sh' >/dev/null 2>&1; then
  echo 'Provider-specific model identifier in committed spec:'
  git grep -nIE 'gpt-[0-9]|claude-[0-9]|gemini-[0-9]' -- ':!local/*.yml' ':!scripts/check.sh'
  fail=1
fi

# 9. Social Draft Pulse consumes provider-neutral social and availability sources,
# with every required read operation expressed as a source capability that setup can
# resolve into the materialized prompt.
SOCIAL_SPEC='docs/automations/social-draft-pulse.md'
for source in social-publishing-source availability-calendar-source; do
  grep -q "<${source}>" "$SOCIAL_SPEC" || err "$SOCIAL_SPEC missing source '${source}'"
  grep -q "<${source}>" docs/automations/_preamble.md || err "_preamble.md missing source '${source}'"
  grep -q "^  ${source}:" local/bindings.example.yml || err "bindings.example.yml missing source '${source}'"
done
DECLARED_SOURCE_CAPABILITIES=$(
  awk '
    /^- Source capabilities:/ { declared=1; next }
    declared && /^  - / { print; next }
    declared && /^    `/ { print; next }
    declared { exit }
  ' "$SOCIAL_SPEC" | grep -oE '`[a-z0-9-]+`' | tr -d '`'
)
if [ -z "$DECLARED_SOURCE_CAPABILITIES" ]; then
  err "$SOCIAL_SPEC declares no source capabilities"
fi
while IFS= read -r capability; do
  [ -n "$capability" ] || continue
  grep -q "${capability}" docs/automations/_preamble.md || err "_preamble.md missing source capability '${capability}'"
  grep -q "${capability}" local/bindings.example.yml || err "bindings.example.yml missing source capability '${capability}'"
done <<< "$DECLARED_SOURCE_CAPABILITIES"
grep -q '## Source capabilities' skills/setup-kb-infra/SKILL.md || \
  err 'setup skill does not compose declared source capabilities'
grep -q '^- Coverage cadence: required' "$SOCIAL_SPEC" || \
  err "$SOCIAL_SPEC does not declare required coverage cadence context"
grep -q '## Coverage cadence' skills/setup-kb-infra/SKILL.md || \
  err 'setup skill does not compose declared coverage cadence context'
if grep -q '<typefully-published-source>' "$SOCIAL_SPEC" docs/automations/_preamble.md; then
  err 'provider-specific Typefully source leaked into the current automation contract'
fi
if grep -Eq 'Wednesday late-afternoon|Thursday and Friday' "$SOCIAL_SPEC"; then
  err "$SOCIAL_SPEC hardcodes a weekday-specific coverage example"
fi

# 10. Provider-neutral executable contracts keep their black-box regression tests.
if ! python3 -m unittest discover -s tests -p 'test_*.py'; then
  err 'audit baseline tests failed'
fi

if [ "$fail" -ne 0 ]; then
  echo "spec check: FAILED"
  exit 1
fi
echo "spec check: OK"
