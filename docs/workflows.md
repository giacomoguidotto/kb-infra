# Workflows

Knowledge Bank Infrastructure defines a small set of agent workflows around the live Notion workspace. Notion remains the source of truth.

## 1. Manual Capture

Trigger: Giacomo manually invokes `/dump-knowledge` or asks to save a conversation/session into the Knowledge Bank.

Flow: use `skills/dump-knowledge`; inspect live Notion structure; draft the smallest coherent Notion update; ask Giacomo to approve the exact draft; write only after approval.

Rules:

- Do not write session knowledge to Notion without explicit confirmation.
- Prefer the existing Notion structure over repo assumptions.
- Keep parent pages thin; put dense knowledge in the right child page.
- Choose one canonical owner for each fact, chapter, or lesson; other pages should link to it instead of duplicating it.

Interactive life-context capture uses `skills/grill-knowledge`: ask one question at a time, produce a Notion draft at the end, and write only after confirmation.

## 2. Live Lookup

Trigger: an agent task may depend on Giacomo's personal, task, project, finance, profile, portfolio, or Knowledge Bank facts.

Flow: perform a narrow live Notion lookup using the available connector, read only the pages or rows relevant to the task, internalize the task-relevant facts, and continue.

Rules:

- There is no automatic repository mirroring step.
- Do not maintain broad replicated knowledge stores.
- Treat repo docs and memory as routing surfaces, not copies of Notion.
- Use `skills/get-knowledge` only when Giacomo explicitly asks to refresh from Notion or when a normal lookup is not enough.

## 3. Drift Audit

Trigger: the scheduled Codex automation `Knowledge Bank Drift Audit`, or a manual request to audit Knowledge Bank drift.

Flow: start from this repo's agent instructions and [Knowledge Bank Conventions](knowledge-bank-conventions.md), inspect the live Notion `life` database and targeted pages, then produce a concise report with findings and exact proposed fixes.

Rules:

- The drift audit is about Knowledge Bank structure and ownership, not access-control or artifact-release reviews.
- Do not write to Notion during the audit.
- Group findings by severity and include page links.
- Propose exact drafts or property changes for Giacomo to approve.

## 4. Portfolio Generation

Portfolio generation is not yet an accepted workflow in this repo. Treat portfolio-related work as project design until Giacomo defines the architecture.
