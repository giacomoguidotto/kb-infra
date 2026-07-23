#!/usr/bin/env bash
# Spec validator for Knowledge System. Checks the source only; the live systems it
# materializes into are out of scope by design (see docs/adr/0001).
set -uo pipefail

fail=0
err() { printf 'FAIL: %s\n' "$*"; fail=1; }

TMP_BROKEN=$(mktemp)
TMP_INTERFACE_DEPS=$(mktemp -d)
trap 'rm -f "$TMP_BROKEN"; rm -rf "$TMP_INTERFACE_DEPS"' EXIT

self=':!scripts/check.sh'

# 1. No machine-specific absolute paths in committed files.
if git grep -nI -e '/Users/' -e '/home/' -- "$self" >/dev/null 2>&1; then
  echo "Absolute home paths in committed files:"
  git grep -nI -e '/Users/' -e '/home/' -- "$self"
  fail=1
fi

# 2. No retired terms (catch renames regressing).
for pat in \
  '/recall' \
  '/remember' \
  'Eval Pulse' \
  'Tuning Audit' \
  'Advancement Pulse' \
  'Knowledge Harvest' \
  'Social Draft Pulse' \
  'Portfolio Surface Sweep' \
  'Job Hunt Evaluate Audit' \
  'Job Hunt Advance Audit'; do
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
for f in skills/public/*/SKILL.md skills/internal/*/SKILL.md; do
  [ -f "$f" ] || continue
  head -6 "$f" | grep -q '^name:' || err "$f missing 'name:' frontmatter"
  head -6 "$f" | grep -q '^description:' || err "$f missing 'description:' frontmatter"
done

# 4a. The provider-blind Knowledge System interface package is internally coherent.
if ! python3 -m pip install --quiet --disable-pip-version-check \
  --target "$TMP_INTERFACE_DEPS" 'jsonschema==4.25.1'; then
  err 'could not install the pinned interface schema validator'
elif ! PYTHONPATH="$TMP_INTERFACE_DEPS${PYTHONPATH:+:$PYTHONPATH}" \
  python3 scripts/check-interface.py; then
  fail=1
fi

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
ADVANCE_SPEC='docs/automations/job-pursue.md'
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
if grep -Eq 'candidacy-select\.mjs|modes/next\.md|career-ops next' "$ADVANCE_SPEC"; then
  err "$ADVANCE_SPEC hardcodes one career-system implementation instead of bound capabilities"
fi
grep -q 'automation body explicitly classifies a narrow in-mandate write' docs/automations/_preamble.md || \
  err '_preamble.md approval rule does not recognize explicitly authorized safe internal writes'

# 8. Every automation declares a provider-agnostic execution profile, and setup has
# a concrete local model binding slot without committing provider model ids.
AUTOMATION_SPECS=(
  skills/public/setup-knowledge-system/resources/automations/kb-reconcile/definition.md
  docs/automations/social-compose.md
  docs/automations/portfolio-refresh.md
  docs/automations/job-scout.md
  docs/automations/job-pursue.md
)
MODEL_EXAMPLE=$(sed -n '/^models:/,/^[a-z][a-z_-]*:/p' local/bindings.example.yml)
for spec in "${AUTOMATION_SPECS[@]}"; do
  profile=$(sed -n 's/^- Execution profile: `\([^`]*\)`.*/\1/p' "$spec")
  case "$profile" in
    frontier/medium|frontier/high|frontier/parallel|balanced/medium|balanced/high|efficient/low|efficient/medium) ;;
    '') err "$spec declares no execution profile" ;;
    *) err "$spec declares unsupported execution profile '$profile'" ;;
  esac
  if [ "$spec" = 'skills/public/setup-knowledge-system/resources/automations/kb-reconcile/definition.md' ]; then
    automation='kb-reconcile'
  else
    automation=$(basename "$spec" .md)
  fi
  grep -q "^  ${automation}:$" <<< "$MODEL_EXAMPLE" || \
    err "bindings.example.yml missing model slot for '${automation}'"
done
if git grep -nIE 'gpt-[0-9]|claude-[0-9]|gemini-[0-9]' -- ':!local/*.yml' ':!scripts/check.sh' >/dev/null 2>&1; then
  echo 'Provider-specific model identifier in committed spec:'
  git grep -nIE 'gpt-[0-9]|claude-[0-9]|gemini-[0-9]' -- ':!local/*.yml' ':!scripts/check.sh'
  fail=1
fi

EVALUATE_SPEC='docs/automations/job-scout.md'
grep -Fq 'node scan.mjs --verify --throttle --max-new=30 --max-per-company=3' "$EVALUATE_SPEC" || \
  err "$EVALUATE_SPEC does not pin the bounded scan command"
grep -q 'Drain the first 30 existing pending/failed items to terminal evaluation states' "$EVALUATE_SPEC" || \
  err "$EVALUATE_SPEC does not drain the selected queue batch to terminal states"
grep -q 'If later existing items remain queued, skip scanning; otherwise run' "$EVALUATE_SPEC" || \
  err "$EVALUATE_SPEC does not skip scanning while existing queue work remains"
grep -q 'Drain every posting selected by the scan to a terminal evaluation state before ending' "$EVALUATE_SPEC" || \
  err "$EVALUATE_SPEC does not drain every selected scan result to a terminal state"
grep -q 'Stop early only for a concrete blocker' "$EVALUATE_SPEC" || \
  err "$EVALUATE_SPEC does not define the sole early-stop condition"

# 9. Social Compose consumes provider-neutral social and availability sources,
# with every required read operation expressed as a source capability that setup can
# resolve into the materialized prompt.
SOCIAL_SPEC='docs/automations/social-compose.md'
for source in social-publishing-source availability-calendar-source external-signal-source; do
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
grep -q '^- Coverage cadence: required' "$SOCIAL_SPEC" || \
  err "$SOCIAL_SPEC does not declare required coverage cadence context"
if grep -q '<typefully-published-source>' "$SOCIAL_SPEC" docs/automations/_preamble.md; then
  err 'provider-specific Typefully source leaked into the current automation contract'
fi
if grep -Eq 'Wednesday late-afternoon|Thursday and Friday' "$SOCIAL_SPEC"; then
  err "$SOCIAL_SPEC hardcodes a weekday-specific coverage example"
fi
grep -q 'Do not schedule a media-dependent draft' "$SOCIAL_SPEC" || \
  err "$SOCIAL_SPEC does not keep media-dependent drafts unscheduled"
grep -q 'reply in this' "$SOCIAL_SPEC" || \
  err "$SOCIAL_SPEC does not define the media-ready reply trigger"
grep -q 'propose a media-independent rewrite' "$SOCIAL_SPEC" || \
  err "$SOCIAL_SPEC does not define the media-independent rewrite path"
OPENING_REVIEW=$(
  awk '
    /^Opening performance and signal review:/ { review=1 }
    review { print }
    review && /^Lookup:/ { exit }
  ' "$SOCIAL_SPEC"
)
[ -n "$OPENING_REVIEW" ] || \
  err "$SOCIAL_SPEC does not start each run with a performance and signal review"
OPENING_REVIEW_LINE=$(grep -n '^Opening performance and signal review:' "$SOCIAL_SPEC" | head -1 | cut -d: -f1)
LOOKUP_LINE=$(grep -n '^Lookup:' "$SOCIAL_SPEC" | head -1 | cut -d: -f1)
if [ -n "$OPENING_REVIEW_LINE" ] && [ -n "$LOOKUP_LINE" ] && \
   [ "$OPENING_REVIEW_LINE" -ge "$LOOKUP_LINE" ]; then
  err "$SOCIAL_SPEC performance and signal review does not precede KB lookup"
fi
grep -q 'post-analytics' <<< "$OPENING_REVIEW" || \
  err "$SOCIAL_SPEC opening review does not read post analytics"
grep -q 'previous pulse' <<< "$OPENING_REVIEW" || \
  err "$SOCIAL_SPEC opening review does not inspect results since the previous pulse"
grep -q 'worked, did not work, or inconclusive' <<< "$OPENING_REVIEW" || \
  err "$SOCIAL_SPEC opening review does not classify what worked and what did not"
grep -q 'external signals' <<< "$OPENING_REVIEW" || \
  err "$SOCIAL_SPEC opening review does not inspect external signals"
grep -q 'hold, refine, test, or realign' <<< "$OPENING_REVIEW" || \
  err "$SOCIAL_SPEC opening review does not require an explicit course-correction decision"
grep -q 'External signals checked' "$SOCIAL_SPEC" || \
  err "$SOCIAL_SPEC does not expose external signals at the approval gate"

# 10. Replacement capture drafts visibly invalidate an explicitly rejected draft.
CAPTURE_SKILL='skills/public/capture/SKILL.md'
CAPTURE_DRAFT='skills/public/capture/HTML-DRAFT.md'
EXAMPLE_DRAFT='assets/example-draft.html'
grep -q 'Every draft generated to replace that rejected draft' "$CAPTURE_SKILL" || \
  err "$CAPTURE_SKILL does not require rejected-draft replacement history"
grep -q 'Previous Draft Invalidated' "$CAPTURE_DRAFT" || \
  err "$CAPTURE_DRAFT is missing the rejected-draft invalidation section"
grep -q 'class="invalidation"' "$EXAMPLE_DRAFT" || \
  err "$EXAMPLE_DRAFT does not demonstrate the invalidation component"
grep -q '>Previous Draft Invalidated<' "$EXAMPLE_DRAFT" || \
  err "$EXAMPLE_DRAFT is missing the exact invalidation heading"
grep -q 'No interpolated value may render as' "$CAPTURE_DRAFT" || \
  err "$CAPTURE_DRAFT does not require escaped text-only interpolation"
grep -q 'Contextually HTML-escape' "$CAPTURE_SKILL" || \
  err "$CAPTURE_SKILL does not require contextual HTML escaping"
grep -q 'invalidation>div { min-width:0; }' "$CAPTURE_DRAFT" || \
  err "$CAPTURE_DRAFT does not let invalidation content shrink on narrow screens"
grep -q 'grid-template-columns:minmax(0,1fr)' "$CAPTURE_DRAFT" || \
  err "$CAPTURE_DRAFT does not collapse invalidation to a shrinkable mobile column"

# 11. Every automation gets a disposable runtime-state file whose completion
# timestamp advances only after the automation reaches its defined end state.
AUTOMATION_STATE_EXAMPLE='local/automation-state.example.yml'
if [ ! -f "$AUTOMATION_STATE_EXAMPLE" ]; then
  err "$AUTOMATION_STATE_EXAMPLE is missing"
else
  grep -q '^last_completed_at:' "$AUTOMATION_STATE_EXAMPLE" || \
    err "$AUTOMATION_STATE_EXAMPLE does not define last_completed_at"
fi
grep -q 'last_completed_at' docs/automations/_preamble.md || \
  err '_preamble.md does not define the completion timestamp rule'
grep -q 'harness-owned automation-local state' docs/automations/_preamble.md || \
  err '_preamble.md does not route completion state to the harness'
grep -q 'resolved automation-local state location' docs/automations/_preamble.md || \
  err '_preamble.md assumes the harness exposes a state file'
if grep -q 'automation-local state file' docs/automations/_preamble.md; then
  err '_preamble.md is not compatible with structured harness state'
fi
grep -q 'harness-owned automation-local state' "$AUTOMATION_STATE_EXAMPLE" || \
  err "$AUTOMATION_STATE_EXAMPLE does not describe harness-owned state"
if grep -q 'local/state' docs/automations/_preamble.md "$AUTOMATION_STATE_EXAMPLE"; then
  err 'automation completion contract still points runtime state into kb-infra/local'
fi
grep -q 'waiting for required approval or clarification' docs/automations/_preamble.md || \
  err '_preamble.md lets reply-gated runs advance the completion timestamp'
grep -q 'blocked, stopped on an error' docs/automations/_preamble.md || \
  err '_preamble.md lets blocked or failed runs advance the completion timestamp'
SETUP_SKILL='skills/public/setup-knowledge-system/SKILL.md'
grep -q 'harness-owned runtime history' "$SETUP_SKILL" || \
  err 'setup skill does not preserve harness-owned runtime history'
grep -q 'existing `last_completed_at` exactly' "$SETUP_SKILL" || \
  err 'setup skill may erase completion history during reconcile'
for spec in skills/public/setup-knowledge-system/resources/automations/kb-reconcile/definition.md docs/automations/job-pursue.md; do
  grep -q '^End state:' "$spec" || \
    err "$spec has no explicit end state for last_completed_at"
done

# 12. Knowledge System owns a self-contained, stateless setup surface.
PUBLIC_SKILLS=(capture lookup setup-knowledge-system)
for skill in "${PUBLIC_SKILLS[@]}"; do
  [ -f "skills/public/$skill/SKILL.md" ] || err "missing canonical public skill '$skill'"
done
for skill in get-knowledge grill-knowledge; do
  [ -f "skills/internal/$skill/SKILL.md" ] || err "missing canonical internal skill '$skill'"
done
[ ! -e skills/setup-kb-infra ] || err 'retired setup-kb-infra source still exists'
[ ! -e local/installed.example.yml ] || err 'retired installed receipt example still exists'
[ ! -e docs/automations/kb-reconcile.md ] || err 'KB Reconcile still has a duplicate top-level definition'

INTERFACE_PACKAGE='skills/public/setup-knowledge-system/resources/knowledge-system-interface/v1'
[ -d "$INTERFACE_PACKAGE" ] || err 'setup module does not carry the v1 interface package'
if find "$INTERFACE_PACKAGE" -name SKILL.md -print -quit | grep -q .; then
  err 'installed interface package would become a fake invocable skill'
fi
grep -Fq '<harness-skill-root>/knowledge-system-interface/v1/' "$SETUP_SKILL" || \
  err 'setup skill does not declare the shared installed interface path'
grep -Fq '<harness-skill-root>/knowledge-system-interface/v1/' skills/public/lookup/SKILL.md || \
  err 'lookup does not resolve the shared installed interface package'
grep -Fq '<harness-skill-root>/knowledge-system-interface/v1/' "$CAPTURE_SKILL" || \
  err 'capture does not resolve the shared installed interface package'

grep -q '/setup-knowledge-system check' "$SETUP_SKILL" || err 'setup skill lacks check mode'
grep -q '/setup-knowledge-system reconcile' "$SETUP_SKILL" || err 'setup skill lacks reconcile mode'
grep -q 'Check is strictly read-only' "$SETUP_SKILL" || err 'setup check is not explicitly read-only'
grep -q 'preserving every existing valid' "$SETUP_SKILL" || err 'setup does not preserve valid bindings'
grep -q 'Only KB Reconcile belongs to this setup' "$SETUP_SKILL" || \
  err 'setup ownership is not limited to KB Reconcile'
grep -q 'zero writes' "$SETUP_SKILL" || err 'setup lacks an identical-second-run no-op contract'
for retired in 'local/installed.yml' 'local/automations/'; do
  grep -q "$retired" "$SETUP_SKILL" || err "setup does not explicitly prohibit $retired"
done

if ! bash scripts/check-setup-idempotency.sh; then
  fail=1
fi

grep -Fq -- '--verify-tag' .github/workflows/ci.yml || \
  err 'release workflow can publish without a verified source tag'

if [ "$fail" -ne 0 ]; then
  echo "spec check: FAILED"
  exit 1
fi
echo "spec check: OK"
