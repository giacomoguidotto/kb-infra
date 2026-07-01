# Job Hunt Evaluate Audit Automation

Prompt source for the scheduled automation that runs the `career-system`
discovery-to-evaluation loop and stops before advancement. Include
[the preamble](_preamble.md) when materializing this automation.

## Design

Job Hunt Evaluate Audit is a discovery-to-evaluation workflow that runs inside the
`career-system` sink.

- KB lookup: not required. This automation runs the career-system's own loop; KB
  context enters later, in Advance and Tune Audits.
- Sink: `<career-system>`.
- Upstream of: Job Hunt Advance Audit.
- Posture: autonomous evaluation output; no application or outreach work.

## Prompt

```md
You are running Job Hunt Evaluate Audit.

The preamble is prepended to this prompt at materialize time.

Setup:
- Read this repo's docs/workflows.md and docs/automations/_preamble.md for the
  boundary.
- Read the career-system sink's own AGENTS.md and data contract before acting.

Goal:
- Run the career-system discovery-to-evaluation loop:
  1. Run the career-system's health check first.
  2. Retry or process existing pending/failed work before scanning.
  3. Scan a bounded batch of new postings only when the queue is drained.
  4. Evaluate live postings.
  5. Generate the expected reports, artifacts, and tracker rows.
  6. Verify the pipeline.

Boundary:
- This is discovery and evaluation only, not advancement or application work.
- Do not submit applications, send messages, click final apply/submit buttons, or
  prefill forms in a hidden or unattended browser.
- Process existing queue work before adding new scan work.

End state:
- Report scan/evaluation results, generated reports and tracker rows, pipeline
  verification status, and blocked actions.
- Hand off advancement to Job Hunt Advance Audit.
```
