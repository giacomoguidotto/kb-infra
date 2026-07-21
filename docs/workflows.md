# Workflows

Knowledge System owns KB Reconcile around the live KB. Other definitions remain in
this map only as migration sources until their owning systems absorb them. Shared
vocabulary and operating rules live in the
[automation preamble](automations/_preamble.md). Cadences and concrete models are
local bindings resolved by the owning setup.

| Automation | Purpose | Output | Spec |
| --- | --- | --- | --- |
| KB Reconcile | Reconcile durable signals from activity | Approval-gated KB Capture | [Definition](../skills/public/setup-knowledge-system/resources/automations/kb-reconcile/definition.md) |
| Social Compose | Turn performance feedback, external signals, and public-safe context into scheduled or media-pending drafts | Social draft queue | [Prompt](automations/social-compose.md) |
| Portfolio Refresh | Compare public-safe context with the portfolio | Reviewed branch/PR work | [Prompt](automations/portfolio-refresh.md) |
| Job Scout | Discover and evaluate opportunities | Career-system reports and rows | [Prompt](automations/job-scout.md) |
| Job Pursue | Produce ranked approach plans and review externally owned waits | Draft application/outreach work and next-route recommendations | [Prompt](automations/job-pursue.md) |

Job Pursue consumes Job Scout output and should run afterward.
Portfolio Refresh is lower-frequency and should be offset from heavier runs.

Each owning setup materializes its source with only the declared endpoints, sinks,
sources, capabilities, cadence context, and shared rules. See
[ADR 0005](adr/0005-materialized-automation-is-self-contained.md).
