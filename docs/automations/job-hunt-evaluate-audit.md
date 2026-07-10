# Job Hunt Evaluate Audit Automation

Prompt source for the scheduled automation that runs the `career-system`
discovery-to-evaluation loop and stops before advancement. Include
[the preamble](_preamble.md) when materializing this automation.

## Design

Job Hunt Evaluate Audit is a discovery-to-evaluation workflow that runs inside the
`career-system` sink.

- KB lookup: narrow. Read `job-search-strategy` to realign the career-system mirror;
  the rest of the career-system loop needs no KB context.
- Endpoints: `job-search-strategy`.
- Sink: `<career-system>` — a mirror sink holding a copy of `job-search-strategy`.
- Execution profile: `balanced/medium` — this is a repeatable orchestration loop
  around sink-native health, queue, scan, evaluation, and verification contracts.
- Startup sync: update the `<career-system>` clone to its remote and confirm a
  clean working tree before the loop runs; then realign the career-system
  `job-search-strategy` copy from the KB. Stop on a non-fast-forward rather than
  running on stale state.
- Mandate: first-party-capture a `job-search-strategy` signal when the loop surfaces
  one (scoring producing weak leads, a drift in target role/seniority/domain/market),
  then realign the mirror. Signal-triggered — most runs capture nothing.
- Absorbs the retired Job Hunt Tune Audit; see
  [ADR 0007](../adr/0007-job-hunt-evaluate-absorbs-tuning.md).
- Upstream of: Job Hunt Advance Audit.
- Posture: autonomous evaluation output; no application or outreach work.

## Prompt

```md
You are running Job Hunt Evaluate Audit.

Read first:
- The career-system sink's own AGENTS.md and data contract.

Startup:
- Before starting the loop, update the career-system clone to its remote: fetch
  and fast-forward to the latest committed state, then confirm the working tree
  is clean.
- If the clone cannot fast-forward cleanly — diverged, dirty, or the remote is
  unreachable — stop and report the concrete blocker rather than running on stale
  state.
- Realign the career-system mirror: /lookup job-search-strategy in context mode and
  update the user-layer config only where the sink's copy has drifted from the KB.
  Propose the realignment in the run summary; apply it as a user-layer change, never
  a shared-default change.

Goal:
- Run the career-system discovery-to-evaluation loop:
  1. Run the career-system's health check first.
  2. Retry or process existing pending/failed work before scanning.
  3. Scan a bounded batch of new postings only when the queue is drained.
  4. Evaluate live postings.
  5. Generate the expected reports, artifacts, and tracker rows.
  6. Verify the pipeline.

Strategy signals (first-party capture):
- While evaluating, watch for signals that the strategy itself should change: scoring
  or scanner config producing too many weak leads, or a drift in target role,
  seniority, domain, market, or baseline compensation.
- When one surfaces, propose a /capture to job-search-strategy for it, then realign
  the career-system copy. This is signal-triggered — if nothing surfaces, capture
  nothing.
- Capture only what this run surfaced explicitly; do not infer across runs, that is
  Knowledge Harvest's job.

Boundary:
- This is discovery and evaluation only, not advancement or application work.
- Do not submit applications, send messages, click final apply/submit buttons, or
  prefill forms in a hidden or unattended browser.
- Process existing queue work before adding new scan work.

End state:
- Report scan/evaluation results, generated reports and tracker rows, pipeline
  verification status, the mirror realignment, any job-search-strategy captures
  proposed, and blocked actions.
- Hand off advancement to Job Hunt Advance Audit.
```
