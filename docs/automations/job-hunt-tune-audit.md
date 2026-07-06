# Job Hunt Tune Audit Automation

Prompt source for the scheduled automation that compares live KB strategy context
with the `career-system` personalization surface and proposes approval-gated
tuning changes. Include [the preamble](_preamble.md) when materializing this
automation.

## Design

Job Hunt Tune Audit is a lookup-to-career-proposal workflow.

- lookup branch: context, once per run.
- Endpoints: `job-search-strategy`, `public-safe-claim-source`, `proof-points`,
  `personal-constraints`, `identity`.
- Sink: `<career-system>` (user-layer configuration only).
- Approval gate: return a tuning summary first. Do not edit repo files or write to
  the KB without approval.
- Empty result: acceptable.

## Prompt

```md
You are running Job Hunt Tune Audit.

Read first:
- The career-system sink's own AGENTS.md, data contract, and user-layer
  configuration.

Goal:
- Pull job-search strategy context from the KB once.
- Inspect the current career-system profile, target roles, scoring preferences,
  scanner configuration, proof points, and public-safe claim boundaries.
- Decide whether the job-search system should change.
- Present a tuning summary for approval before any repo edits.
- Do not apply changes, write to the KB, submit applications, or send messages.

Lookup:
- Use /lookup in context mode over: job-search-strategy, public-safe-claim-source,
  proof-points, personal-constraints, identity.
- Treat job-search-strategy as the private strategy and scoring owner.
- Treat public-safe-claim-source as the adapter for recruiter-facing claims.

Tuning signals:
- New or stronger public proof that should affect targeting or draft packs.
- New personal-constraints (time, location, relocation, work authorization,
  compensation, side-project/IP freedom, references, availability).
- A material change in target role, domain, seniority, market, or baseline
  compensation.
- Tracker/report patterns suggesting the scanner or scoring weights produce too
  many weak leads.

Tuning summary gate:
- Before editing files, return a compact tuning summary: KB/source evidence
  checked, career-system files checked, proposed changes grouped by file, what
  stays stable, public-safety notes, expected effect on scanning/scoring/packs,
  and validation plan.
- Ask the user to approve, reject, or edit the set. Do not edit files until
  approved.

After approval:
- Apply only the approved repo changes. Keep personalization in user-layer files.
- Run the career-system's own validation when the changes touch configuration,
  modes, scanner behavior, tracker behavior, or reports.
- Do not write to the KB. If a KB gap is discovered, report it as a handoff to
  /capture.

End state:
- If no useful candidates exist, say so and include the evidence checked.
- Otherwise stop at the tuning summary and wait for approval.
- After approval, report changed files, validation status, blocked actions, and
  any KB handoff candidates.
```
