# Workflows

Knowledge Bank Infrastructure defines a small set of agent workflows around the live Notion workspace. Notion remains the source of truth.

## 1. Manual Capture

Trigger: Giacomo manually invokes `/remember` or asks to save a conversation/session into the Knowledge Bank.

Flow: use `skills/remember`; inspect live Notion structure; draft the smallest coherent Notion update; ask Giacomo to approve the exact draft; write only after approval.

Rules:

- Do not write session knowledge to Notion without explicit confirmation.
- Prefer the existing Notion structure over repo assumptions.
- Keep parent pages thin; put dense knowledge in the right child page.
- Choose one canonical owner for each fact, chapter, or lesson; other pages should link to it instead of duplicating it.

## 2. Knowledge Bank Drift Realignment

Trigger: the scheduled Codex automation `Knowledge Bank Drift Realignment`, or a manual request to find and resolve stale, missing, due, raw, ambiguous, or project-drift knowledge.

Flow: start from this repo's agent instructions, [Knowledge Bank Conventions](knowledge-bank-conventions.md), `/recall`, and `/remember`. Use `/recall` in clarification mode over live Notion and the `build` page `Subtasks`; compare build projects against recent local git history or remote history when useful. Ask Giacomo one question at a time, then hand answered updates, marker candidates, discarded findings, and unresolved questions to `/remember` for an exact approval draft.

Rules:

- This is a scheduled clarification-to-remember loop, not a report-only audit.
- Do not write to Notion during recall or before `/remember` approval.
- Treat due follow-up markers as questions for Giacomo, not as permission to update the Knowledge Bank.
- A normal discard leaves no KB trace; deferrals and final-form decisions become marker candidates only through approved `/remember` writes.
- Use ignored local scratch only for mechanical hints such as last run time or commit cursors. Never store copied KB facts, answered questions, suppressions, or durable reports in local state.
- The scheduled prompt source lives in [Knowledge Bank Drift Realignment Automation](automations/kb-drift-realignment.md).

## 3. Portfolio Generation

Portfolio generation is not yet an accepted workflow in this repo. Treat portfolio-related work as project design until Giacomo defines the architecture.
