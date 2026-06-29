---
name: recall
description: Recall live KB context from Notion without writing. Use when a task or automation needs scoped Knowledge Bank facts, caller-defined evidence checks, or optional clarification for unresolved knowledge.
---

# Recall

## Purpose

Recall is a read-only retrieval primitive for the Notion Knowledge Bank. It returns scoped KB context by default and clarifies unresolved knowledge only when the caller asks for that detour.

## Branches

- `context`: retrieve relevant KB context for the caller. Do not ask questions unless a missing fact blocks the task and clarification is allowed.
- `clarification`: build a caller-relevant queue, then ask Giacomo one question at a time.

## Workflow

### 1. Set Scope

Identify the caller's objective, recall surface, and branch. The surface can be a named page, life area, project, workflow, automation run, or broad KB pass.

For project recall, use the Notion `build` page and its `Subtasks` when the caller's scope includes build projects or portfolio/project drift. For broad recall, use normal workspace search and targeted fetches over the live Notion workspace. SQL/data-source querying is an optional optimization, not a dependency.

Completion criterion: the branch, recall surface, Notion anchors, project anchors, and connector limits are stated.

### 2. Search Live KB

Use the Notion connector and fetch likely pages before judging them. Search from the caller's objective outward: named pages, likely canonical owners, parent/child pages, relations, project pages, and relevant sibling examples. Skip final form sections entirely unless Giacomo explicitly reopens them.

Look for:

- relevant canonical facts for the caller's task
- page ownership and placement context
- status, dates, markers, or properties that the caller asked recall to consider
- evidence that the caller's current task depends on a missing, stale, or ambiguous KB fact
- related pages that help avoid duplicate or contradictory context

Do not broaden into caller-irrelevant audits. Recall supplies the retrieval pattern; callers supply their own signal policy.

Completion criterion: every retained source or candidate has fetched Notion evidence, external evidence, or an explicit `unverified` note, and every searched area is tied to the caller's objective.

### 3. Compare External Evidence

Only compare external evidence when the caller asks for it or the recall surface requires it. For project drift, compare the project page with recent local git history if the clone is available. If the local clone is missing or stale, use remote history when available. Ignore purely mechanical churn unless it changes durable project state.

Completion criterion: every external comparison explains whether it produced relevant KB context, a candidate gap, or no durable signal.

### 4. Classify

Classify retained candidates with the smallest useful state:

- `relevant`: context the caller can use now.
- `missing`: the KB lacks a fact or context implied by the evidence.
- `stale`: the KB states an old current state.
- `scheduled`: a dated task, deadline, marker, or caller-defined time signal appears due or past.
- `deferred`: a caller-defined marker or question has a future date.
- `already-handled`: the canonical KB page already contains the resolved state.
- `maybe`: the evidence is weak, but the finding may reveal stale or incomplete KB context.
- `uncertain`: the evidence is too weak or ambiguous to classify further.

Answer outcomes used only in the clarification branch:

- `discard`: Giacomo says the finding is not worth carrying forward; no KB write is needed.
- `final-form`: Giacomo says the topic should not be questioned again; produce a final form marker candidate for the caller.

Do not use local automation state to suppress knowledge questions. The KB is the ledger; unapproved or unresolved questions may be found again.

Completion criterion: every retained item has one classification, one short rationale, and a next action.

### 5. Return Context

For the `context` branch, return a compact recall packet:

```md
Sources:
- <Notion page/search/external source>

Context:
- <fact or page-specific context the caller can use>

Gaps:
- <missing/stale/ambiguous item, only if relevant to the caller>

Use:
- <how this should affect the caller's next step>
```

Do not include final form sections in the packet. Do not ask a clarification question from this branch unless the caller allowed clarification and the gap blocks the task.

Completion criterion: the caller has enough KB context to continue, or the blocking gap is explicit.

### 6. Clarify Gaps

For the `clarification` branch, build the complete question queue before asking Giacomo. Group questions by the caller's register and priority policy. When no policy is provided, order the queue:

1. Blocking gaps for the caller's current task.
2. Due caller-defined markers or dated signals.
3. Externally evidenced mismatches.
4. Personal or identity-level questions.
5. Other missing, stale, ambiguous, or low-confidence candidates.

Before the first question, state the total queue count and the first group being handled. Run the queue like a `grill-me` decision tree. Ask one question, wait for Giacomo's answer, classify the answer, then choose the next branch. If an answer raises a more important follow-up, ask that follow-up before moving to the next queued item. Do not dump the full queue unless Giacomo asks for it.

Use a soft cap of 10 questions per clarification sitting unless the caller specifies another limit. When the cap is reached, state how many queued questions remain and ask whether to continue now or defer the rest.

Completion criterion: every queued item is answered, deferred, discarded, converted into a final form marker candidate, or left as an explicit unresolved question.

### 7. Return Clarification Results

Return structured results to the caller. Recall does not choose the downstream write workflow. For marker candidates, use the marker formats in [docs/knowledge-bank-conventions.md](../../docs/knowledge-bank-conventions.md).

```md
Answered updates:
- <durable KB update candidate>

Follow-up marker candidates:
- <date, target, prompt, rationale>

Final form marker candidates:
- <target, scope, rationale>

Discarded:
- <finding discarded without KB trace>

Unresolved:
- <question still open>
```

Completion criterion: the caller can hand the result to its own approval, write, or planning flow without hidden context.

## Rules

- Notion is canonical; repo docs and memory are routing surfaces.
- Read broadly enough to satisfy the caller, but fetch only pages that are plausible sources or candidates.
- Never write to Notion from recall.
- Do not invent exact dates from relative phrases.
- Do not duplicate KB knowledge into local state.
- If the caller makes recall stateful, treat local state as replaceable hints for the next run; deleting it must make recall slower, not less correct.
