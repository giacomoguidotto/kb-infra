# Career Ops knowledge duplication inventory

Research for GitHub issue 44, observed on 2026-07-16. This was a read-only
comparison of the current Career Ops user layer with narrow live Knowledge Bank
reads. No Knowledge Bank or Career Ops data was changed.

## Answer

Career Ops contains three kinds of user data that need different treatment:

1. **Knowledge System mirrors:** personal facts, public-safe claims, proof points,
   opportunity strategy, personal constraints, and communication rules copied from
   Knowledge Bank owners.
2. **Career Ops operational state:** applications, evaluations, attempts, outcomes,
   queues, reports, and Career Ops-specific runtime configuration.
3. **Mixed files:** user-layer files where mirrored knowledge and operational
   configuration share one document.

The existing Knowledge System contract understates the mirror. It calls the Career
System a copy of `job-search-strategy`, but the current Career Ops user layer also
copies `identity`, public-safe profile and proof, personal constraints,
communication strategy, and project evidence.[^ks-contract] A safe reconciler must
therefore update an explicit allowlist of mirror fields and leave Career Ops state
alone.

## Exact mirror inventory

| Career Ops surface | Exact fields or sections | Knowledge System owner | Current assessment |
| --- | --- | --- | --- |
| `config/profile.yml` | `candidate.full_name`, `preferred_name`, `email`, `phone`, `location`, `linkedin`, `portfolio_url`, `github` (lines 4-13) | `identity`; public profile adapter for reusable links | Duplicate. Values were broadly aligned in this read. `x_url` was not verified against the fetched identity page. |
| `config/profile.yml` | `application_form_defaults.*` (lines 15-23) | `identity` EEO and demographic form policy | Duplicate with drift. See findings 1 and 2. |
| `config/profile.yml` | `target_roles.primary`, `target_roles.archetypes.*` (lines 32-62) | Opportunity Preferences, especially Role Fit | Duplicate. Broadly aligned, but the local representation is more prescriptive. |
| `config/profile.yml` | `narrative.*`, including headline, exit story, superpowers, and proof points (lines 64-86) | public profile adapter plus the linked employment, education, credential, and project owners | Duplicate. It is a useful Career Ops projection, not an independent owner. |
| `config/profile.yml` | `compensation.*` (lines 88-92) | Opportunity Preferences / Compensation and Location | Duplicate. The 30% risk-adjusted threshold currently matches. |
| `config/profile.yml` | `location.country`, `city`, `visa_status`, `relocation_openness`, `onsite_availability` (lines 94-100) | `identity`, Location, Work Authorization And Relocation | Duplicate. `timezone` is Career Ops-local runtime context unless another owner is established. |
| `config/profile.yml` | `cover_letter.notice_period_days`, `primary_domain` (lines 108-110) | Danfoss Admin for notice; public profile and work evidence for positioning | Duplicate with drift in the notice-period certainty. |
| `modes/_profile.md` | Your Target Roles, Adaptive Framing, Role-shape boundary, Exit Narrative, Cross-cutting Advantage (lines 13-58) | Opportunity Preferences and public profile | Duplicate. |
| `modes/_profile.md` | Outreach Voice Notes (lines 60-68) | Communication Strategy | Duplicate. The LinkedIn-specific example can remain a Career Ops specialization, but the general voice rules are canonical in the KB. |
| `modes/_profile.md` | Portfolio / Demo, Project Maturity Gate, Project Eligibility Snapshot (lines 70-101) | public profile adapter and canonical project pages | Duplicate and highly drift-prone because project maturity changes independently. |
| `modes/_profile.md` | Comp Targets, Negotiation Scripts, Location Policy, Seniority Policy (lines 103-163) | Opportunity Preferences and its Compensation, Location, and Work Authorization children; Communication Strategy for authoring | Duplicate. Scripts are Career Ops output material, while the preferences and rules they encode are mirrors. |
| `modes/_profile.md` | Public Claim Guardrails (lines 165-169) | public profile adapter and evidence owners | Duplicate. |
| `modes/_custom.md` | Evaluation And Advancement Policy and Hard skips (lines 35-83) | Opportunity Preferences | Duplicate. Other sections in this file are mostly Career Ops-owned procedure. |
| `voice-dna.md` | Whole file, especially Writing Rules, Formatting Rules, and banned patterns (lines 1-223) | Communication Strategy | Competing owner. The file explicitly calls itself the voice source of truth, while the KB page is canonical for cross-surface voice and authoring. |
| `portals.yml` | `title_filter.positive`, `title_filter.negative`, `title_filter.seniority_boost` (lines 98-230) | Opportunity Preferences target roles, title/seniority policy, tech-stack policy, and hard rejects | Materialized strategy with current drift. Search sources and company lists are Career Ops operational configuration, but these filters encode KB-owned policy. |
| `cv.md` | Identity header and every substantive CV section (lines 1-79) | `identity`, public profile adapter, and linked work, education, credential, and project pages | Derived public artifact. Career Ops needs a local CV, but it must not become the fact owner. |
| `article-digest.md` | Current Positioning, Danfoss, AnyPINN, Knowledge Bank Infrastructure, Education And Signal, and Supporting Projects (lines 5-57) | public profile adapter and linked canonical evidence/project owners | Derived proof projection. Career Ops-specific instructions about when to use evidence can remain local. |

Career Ops itself defines all of these as protected user-layer data rather than
system files.[^career-data-contract] That protects them from upstream updates, but
it does not prevent drift from the Knowledge System.

## Verified current drift

### 1. Voluntary demographic default conflicts with the KB

`config/profile.yml` places actual demographic answers under
`application_form_defaults`.[^profile-demographics] The live `identity` owner says
the default voluntary demographic answer is `Prefer not to answer`, with review
required unless an explicit default is set.[^kb-identity] Career Ops therefore
encodes disclosure as the local default while the canonical source encodes
non-disclosure.

### 2. Career Ops contains demographic fields with no fetched canonical owner

Pronouns, sexual orientation, and transgender status are populated in
`application_form_defaults`, but those fields were absent from the fetched
`identity` page.[^profile-demographics] They may be valid facts, but they are
unverified from the declared owner and should not be treated as synchronized.

### 3. Notice period loses the KB's uncertainty

Career Ops stores `notice_period_days: 30` as an exact value.[^profile-notice]
Danfoss Admin records only that the period is usually one month and explicitly
requires checking the contract before relying on it.[^kb-danfoss] The mirror has
turned a verify-before-use note into a precise application default.

### 4. Scanner hard rejects contradict weighted strategy

The live Opportunity Preferences page says to use very few hard rejects. Junior
titles and internships are negative weights, unfamiliar stacks should remain
reviewable, and PHP is the only stack-specific hard reject recorded there.[^kb-opportunity]
`portals.yml` rejects Junior, Intern, Graduate, New Grad, multiple stacks besides
PHP, and broad seniority/title classes before evaluation.[^portals-negative]
This changes a weighted policy into an irreversible discovery gate.

The same filter positively admits `KI Trainer`, `Dozent`, and `Weiterbildung`, while
the KB targets technical IC roles and excludes non-engineering professions from
target-positive search.[^portals-positive] This is evidence that the discovery
projection has accumulated older or broader targeting policy.

### 5. The synchronization contract is narrower than the actual copies

Job Scout currently promises to reconcile `job-search-strategy` into user-layer
configuration.[^job-scout] That does not cover the duplicated identity, profile,
proof, project-maturity, personal-constraint, and communication surfaces above.
The current drift is therefore structural, even where individual values happen to
match today.

## Career Ops data that is not a Knowledge System mirror

The following is Career Ops-owned operational state and should remain outside a
Knowledge System to Career Ops overwrite:

- `data/applications.md`: application lifecycle state and tracker rows.
- `data/pipeline.md`: pending URL inbox.
- `data/scan-history.tsv` and `data/scan-runs.tsv`: discovery deduplication and run
  observations.
- `data/follow-ups.md` and `data/approach-attempts.md`: confirmed follow-up and
  outreach-attempt history.
- `data/candidacy-clusters.md`: evidence-backed coordination among related
  applications.
- `data/offers/*`, `data/salary-observations.tsv`, `data/status-log.tsv`, and
  `data/assessments.tsv`: process and outcome evidence.
- `reports/*`, `interview-prep/*`, `output/*`, `jds/*`, and `writing-samples/*`:
  opportunity-specific evidence and generated work product.
- `config/profile.yml` keys `application_history.*`, `language.*`, `cv.*`,
  `auto_pdf_score_threshold`, and Career Ops-specific formatting limits.
- `portals.yml` provider mechanics, enabled sources, tracked-company inventory,
  dedup settings, and scanner runtime configuration. Only policy-bearing filters
  and query intent are strategy projections.
- `modes/_custom.md` Candidacy Coordination Policy, report-shape contract, concrete
  CV rendering rules, and application-pack workflow rules where they describe
  Career Ops procedure rather than personal facts or cross-surface strategy.

Career Ops documents the tracker, pipeline, reports, and local files as its own
permanent file-based source of truth.[^career-architecture] Knowledge System
reconciliation should never rewrite these based on KB inference.

## Reconciliation boundary implied by the evidence

A future `/setup-career-system` can stay simple and idempotent if it owns an
explicit field and section map:

- Onboarding: materialize the mirror-backed portions of `config/profile.yml`,
  `modes/_profile.md`, `voice-dna.md`, `cv.md`, and `article-digest.md` only when
  the Career Ops user layer is fully absent.
- Reconciliation: compare live KB owners with only the allowlisted mirror fields,
  present the exact delta, and update only changed mirror content after approval.
- Validation: flag unsupported local values and policy projections such as
  `portals.yml` filters without rewriting Career Ops state.
- No-op: when owner values and projections already agree, write nothing.

The exact generated representation is still unresolved. In particular,
`modes/_profile.md`, `voice-dna.md`, and the CV combine canonical meaning with
Career Ops-specific prose. A later design ticket should decide between replacing
whole marked sections and maintaining finer field-level projections.

## Sources

[^ks-contract]: Knowledge System endpoint and sink contract,
    [`docs/automations/_preamble.md:61-101`](../automations/_preamble.md).
[^job-scout]: Knowledge System Job Scout realignment contract,
    [`docs/automations/job-scout.md:12-24`](../automations/job-scout.md) and
    [`docs/automations/job-scout.md:38-48`](../automations/job-scout.md).
[^career-data-contract]: Career Ops data contract,
    `/Users/giacomo/dev/life/career-ops/DATA_CONTRACT.md:3-44`.
[^career-architecture]: Career Ops architecture,
    `/Users/giacomo/dev/life/career-ops/ARCHITECTURE.md:13-24` and
    `/Users/giacomo/dev/life/career-ops/ARCHITECTURE.md:46-58`.
[^profile-demographics]: Current Career Ops profile,
    `/Users/giacomo/dev/life/career-ops/config/profile.yml:15-23`.
[^profile-notice]: Current Career Ops profile,
    `/Users/giacomo/dev/life/career-ops/config/profile.yml:108-110`.
[^portals-positive]: Current Career Ops scanner positive filters,
    `/Users/giacomo/dev/life/career-ops/portals.yml:98-155`.
[^portals-negative]: Current Career Ops scanner negative and seniority filters,
    `/Users/giacomo/dev/life/career-ops/portals.yml:156-230`.
[^kb-identity]: Live KB `identity` page, fetched read-only on 2026-07-16:
    <https://app.notion.com/p/376a3ade6b99819a982ac87706af97f6>.
[^kb-opportunity]: Live KB `Opportunity Preferences` page, fetched read-only on
    2026-07-16: <https://app.notion.com/p/384a3ade6b99811abd04dcf9ebe3cefd>.
[^kb-danfoss]: Live KB `Danfoss Admin` page, fetched read-only on 2026-07-16:
    <https://app.notion.com/p/287a3ade6b9980d784bdebbc6c8f07cb>.

