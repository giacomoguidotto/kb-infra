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

## 2. Recall

Trigger: a workflow or automation needs relevant Knowledge Bank context, or Giacomo asks what the Knowledge Bank is missing, stale, or ready to revisit.

Flow: use `skills/recall`; retrieve scoped live Notion context for the caller. If the caller explicitly needs hole-filling or stale-state resolution, use recall's clarification branch to build a complete question queue and ask Giacomo one question at a time.

Rules:

- Recall reads broadly enough to satisfy the caller, but does not mirror the Knowledge Bank locally.
- Treat the Knowledge Bank as the ledger for `already handled`: resolved questions should be reflected in canonical Notion pages, and deferred questions should be reflected as follow-up markers.
- Do not write to Notion during recall.

## 3. Drift Audit

Trigger: the scheduled Codex automation `Knowledge Bank Drift Audit`, or a manual request to audit Knowledge Bank drift.

Flow: start from this repo's agent instructions and [Knowledge Bank Conventions](knowledge-bank-conventions.md), inspect the live Notion `life` database and targeted pages, then produce a concise report with findings and exact proposed fixes.

Rules:

- The drift audit is about Knowledge Bank structure and ownership, not access-control or artifact-release reviews.
- Do not write to Notion during the audit.
- Treat due follow-up markers as questions for Giacomo, not as permission to update the Knowledge Bank.
- Group findings by severity and include page links.
- Propose exact drafts or property changes for Giacomo to approve.

## 4. Portfolio Generation

Portfolio generation is not yet an accepted workflow in this repo. Treat portfolio-related work as project design until Giacomo defines the architecture.
