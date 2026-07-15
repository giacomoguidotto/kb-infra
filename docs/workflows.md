# Workflows

Knowledge Bank Infrastructure defines five automations around the live KB. Their
source files are the specification; this page is only the map. Shared vocabulary
and operating rules live in the [automation preamble](automations/_preamble.md).
Cadences and concrete models are local bindings resolved by setup.

| Automation | Purpose | Output | Spec |
| --- | --- | --- | --- |
| Knowledge Harvest | Reconcile durable signals from activity | Approval-gated KB Capture | [Prompt](automations/knowledge-harvest.md) |
| Social Draft Pulse | Turn performance feedback, external signals, and public-safe context into scheduled drafts | Social draft queue | [Prompt](automations/social-draft-pulse.md) |
| Portfolio Surface Sweep | Compare public-safe context with the portfolio | Reviewed branch/PR work | [Prompt](automations/portfolio-surface-sweep.md) |
| Job Hunt Evaluate Audit | Discover and evaluate opportunities | Career-system reports and rows | [Prompt](automations/job-hunt-evaluate-audit.md) |
| Job Hunt Advance Audit | Produce ranked approach plans and review externally owned waits | Draft application/outreach work and next-route recommendations | [Prompt](automations/job-hunt-advance-audit.md) |

Job Hunt Advance Audit consumes Evaluate Audit output and should run afterward.
Portfolio Surface Sweep is lower-frequency and should be offset from heavier runs.

Setup materializes each source with only its declared endpoints, sinks, sources,
capabilities, cadence context, and shared rules. See
[ADR 0005](adr/0005-materialized-automation-is-self-contained.md).
