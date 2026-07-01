---
name: setup-kb-infra
description: Materialize and reconcile Knowledge Bank Infrastructure on this machine. Connect the KB provider, collect bindings, install the lookup and capture skills, and bootstrap the automations — on first run and on every later run. Use when the user runs /setup-kb-infra, says bootstrap/install/wire up kb-infra, or asks to update, sync, reconcile, or health-check the setup.
---

# Setup

## Purpose

Setup materializes the spec into a working setup on this machine and keeps it in
sync over time. It is a **reconcile**, not a one-shot installer: it reads the
desired state from the spec (the source of record), reads the actual materialized
state, and closes the gap. The first run reconciles from nothing; every later run
reconciles from whatever already exists. It writes only gitignored `local/`
bindings and the user's own harness config; it never commits a personal value.

This mirrors the plan/apply model behind ADR 0001's Terraform analogy: compute the
drift, show it, then apply only the delta.

## Branches

- `all` (default): full reconcile — plan, then apply across every element.
- `check`: read-only health check — report drift and stop; change nothing.
- scoped: reconcile one element — `provider`, `bindings`, `skills`, or a named
  automation.

Run the full reconcile unless the user scopes it. Later steps assume earlier
bindings exist; if a scoped run needs a missing binding, collect it first. Every
step is idempotent: touch only what is missing, changed, or newly added, and leave
correct state alone.

## Workflow

### 1. Plan: diff desired against actual

Compare the spec (desired) with the materialized state (actual) and produce a drift
report before changing anything:

- Version: read the current spec version from the git tags (`git describe --tags`);
  `vX.Y.Z` tags are the source of truth. Compare it against the `version` recorded
  in `local/installed.yml` to see how far the installed setup has fallen behind.
- Desired: the endpoint and sink vocabulary in
  [_preamble.md](../../docs/automations/_preamble.md), the endpoints and sinks each
  **enabled** automation declares, the skills under `skills/`, the automations under
  `docs/automations/`, and one cadence per enabled automation.
- Actual: `local/bindings.yml`, `local/installed.yml`, the snapshotted prompts under
  `local/automations/`, and the installed skill copies.
- Drift to surface, by category:
  - the spec version has advanced past the installed version;
  - endpoints an enabled automation needs but `bindings.yml` leaves unbound (new or
    never-bound);
  - bindings whose endpoint or sink is no longer in the spec (retired);
  - existing bindings that no longer resolve live in the KB (stale);
  - skills whose source differs from the installed copy (stale install) or is not
    installed;
  - automations new to the spec, or whose fresh compose differs from the snapshot in
    `local/automations/`, or removed from the spec;
  - cadences or sinks missing for an enabled automation.

In `check` mode, report this plan and stop.

Completion criterion: the user sees a categorized drift report and nothing has
changed yet.

### 2. Connect the KB Provider

Confirm which provider backs this instance. Validate the connector by reading one
real page. Record the provider and a start hint in `local/bindings.yml` if it is not
already present and valid.

Completion criterion: a live read from the provider succeeded, or the exact
connector blocker is reported.

### 3. Reconcile the Endpoint Bindings

Read the endpoint vocabulary from
[_preamble.md](../../docs/automations/_preamble.md). Bind only the endpoints the
plan flagged as unbound, ambiguous, or stale. Explore the KB to locate a canonical
owner for each; where an owner is missing or ambiguous, grill the user one question
at a time, like `grill-me`, rather than guessing — including for brand-new pages the
user must create (for example a persona or published-context surface). Record each
binding as a hint in `local/bindings.yml`; `lookup` resolves the rest live. Leave
already-valid bindings untouched. Propose removing bindings for retired endpoints;
do not delete a personal value without confirmation.

Completion criterion: every endpoint an enabled automation needs is bound to a KB
location or explicitly marked unbound with a reason, and retired bindings are
resolved.

### 4. Reconcile the Sink Bindings

Read the sink vocabulary from the preamble. For each sink an enabled automation
targets, confirm its link and local clone path, collecting only what the plan
flagged as missing, disabled-yet-needed, or unreachable. Record them in
`local/bindings.yml`.

Completion criterion: every sink an enabled automation needs has a binding, or is
marked disabled.

### 5. Reconcile the Installed Skills

Copy `lookup`, `capture`, and `setup-kb-infra` into the harness skill directory,
re-copying only those whose source differs from the installed copy. Prefer
`~/.agents/skills/<name>/` and `~/.claude/skills/<name>/`, which together cover
current harnesses. Use materialized copies, not symlinks or hard links.

Confirm the `capture` approval-draft styling on first run: the shipped default is a
dark, Notion-style palette. Ask the user whether it works or whether they want it
restyled, and record the choice in `local/bindings.yml`; do not re-ask once it is
recorded.

Completion criterion: each skill's installed copy matches its source, and the
draft-style choice is recorded.

### 6. Reconcile the Automations

For each enabled automation, compose the paste-ready prompt from three parts: the
preamble, the automation body, and the resolved bindings. Confirm the cadence
binding. Detect the harness: if it can create a scheduled automation from an agent,
create or update it; otherwise output the paste-ready prompt and name where it goes.
Recreate only automations the plan flagged as new, changed, or cadence-drifted, and
offer to retire automations removed from the spec. After applying, snapshot each
installed automation's composed prompt to `local/automations/<name>.md` and update
`local/installed.yml` with the current spec version, timestamp, and per-automation
cadence and hash, so the next run can compute drift.

Completion criterion: every enabled automation is created, updated, or handed over
as a paste-ready prompt with its target and cadence, and `local/installed.yml` plus
the `local/automations/` snapshots are current.

### 7. Report

Report the plan applied: what changed, every binding recorded or removed, every
skill re-copied, every automation created, updated, retired, or handed over, and
anything still unbound or drifted.

Completion criterion: the user can see the full state of the setup, what the
reconcile changed, and the exact next manual action, if any.

## State

- The spec version lives in the git `vX.Y.Z` tags, not in a committed file; read it
  with `git describe --tags`. `scripts/bump-version.sh` advances it from conventional
  commits.
- Record the installed state in gitignored `local/installed.yml` (spec version,
  timestamp, and per-automation cadence and content hash) with the composed prompts
  snapshotted under `local/automations/`, per the preamble State Model. Use it only
  to compute drift; never store copied KB facts, answered grill questions, or
  anything beyond the version, cursors, and installed prompts themselves.
- Deleting the record must not make the next run less correct — only slower, by
  forcing a full re-materialize.

## Rules

- Write bindings only to gitignored `local/`. Never commit a personal value.
- Never write a personal value into a committed spec file.
- Be idempotent: a re-run with no spec change and healthy state makes no changes and
  grills nothing.
- Do not re-grill bindings that are already recorded and still resolve.
- `check` mode is read-only: it plans and reports, and writes nothing.
- Retire, don't orphan: when an endpoint, sink, or automation leaves the spec,
  propose removing its materialized counterpart, but delete a personal value only
  with confirmation.
- Use [bindings.example.yml](../../local/bindings.example.yml) as the shape for
  `local/bindings.yml`, and
  [installed.example.yml](../../local/installed.example.yml) as the shape for
  `local/installed.yml`.
- The follow-up marker policy ships as a repo default; offer to override it into a
  binding, do not assume.
- Treat `local/bindings.yml` as replaceable: re-running setup rebuilds it from the
  live KB and the user's answers.
