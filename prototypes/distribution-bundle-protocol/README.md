# Prototype: CI-only Distribution Bundle publication protocol

This is throwaway logic for issue #43. It asks whether a level-triggered,
single-writer GitHub Actions workflow can safely publish `giacomoguidotto/skills`
without turning release notifications into an ordered event log or introducing a
synchronized constellation release manifest.

Run every hard-case scenario with:

```bash
bash prototypes/distribution-bundle-protocol/run.sh --all
```

Run the interactive state viewer with:

```bash
bash prototypes/distribution-bundle-protocol/run.sh
```

The prototype does not call GitHub or publish anything. It keeps all state in
memory and models the proposed workflows in `workflows/`.

## Candidate decision

Treat every source release notification as a wake-up hint. The Distribution
Bundle workflow ignores payload content when choosing inputs, rereads the latest
stable immutable release of every repository in a committed positive allowlist,
and rebuilds the entire `skills/` tree in a temporary directory. Publication is
one atomic commit to `giacomoguidotto/skills/main`; that commit SHA is the bundle
version.

The allowlist contains repository identities and export paths, never source
versions:

- Agentic OS, Knowledge System, and Mastery System export
  `skills/public/*`.
- The `giacomoguidotto/career-ops` fork exports only
  `skills/public/setup-career-system`.
- `.agents/skills`, Career Ops operational skills, and `santifer/career-ops`
  releases are never scanned.

The generated `provenance.lock.json` records each source release ID, tag, commit
SHA, archive digest, exported path, and exported tree digest. It omits timestamps
so an unchanged rebuild is a true no-op. Source releases must have GitHub's
immutable-release flag; a mutable, missing, draft, or prerelease source blocks
publication and leaves the current bundle untouched.

Live API checks on 2026-07-20 found immutable releases disabled on Knowledge
System, Mastery System, and the Career Ops fork; Agentic OS and the bundle
repository do not exist yet. Enabling immutable releases on every source is
therefore a migration prerequisite, not an already-satisfied assumption.

## State transitions

1. A source publishes an immutable stable release.
2. Its release workflow mints a short-lived Trigger App installation token scoped
   to `giacomoguidotto/skills` with Actions write only, then invokes the target
   `workflow_dispatch` reconciliation entrypoint.
3. The bundle workflow serializes publication with one running and one pending
   reconciliation. Coalescing is safe because every run computes the full latest
   desired state. A nightly reconciliation repairs missed notifications.
4. CI validates the complete candidate tree before touching `main`: every
   directory has a valid `SKILL.md`, the directory and declared skill names agree,
   and no two sources own the same name.
5. A validation or fetch failure publishes nothing. An identical desired state
   publishes nothing. A changed valid state replaces `skills/`, writes
   provenance, and creates one generated commit.

The Publisher App is the only generated-tree writer. Its Contents-write private
key exists only in the bundle repository; source repositories receive only the
separate Trigger App key, which cannot write repository contents. A `main`
ruleset requires normal human changes to arrive through reviewed pull requests,
blocks deletion and force-pushes, and gives only the Publisher App an always-allow
bypass. A required guard check rejects human pull requests that touch generated
`skills/` or provenance. Manual rollback crosses a protected
`distribution-rollback` environment before minting the Publisher token.

Removing a public skill therefore requires a new immutable source release that
omits it. The next full rebuild removes it from the bundle. A collision fails
closed and preserves the previous bundle.

Rollback is an explicitly authorized manual workflow that restores the generated
tree and provenance from a prior bundle commit as a new commit on `main`. It never
moves a tag, rewrites history, or edits a source-version pin. The next normal
source release reconciliation returns to the latest valid source state, so a
durable source rollback is published as a new source release containing the
reverted content.

Two App identities are the smallest strict authorization boundary. Reusing the
Publisher App key in every source repository would let any compromised source
workflow mint the same Contents-write token that bypasses the bundle ruleset.
The two roles are credentials and repository permissions only; neither adds a
service or control plane.

## Why the bundle has no SemVer

The bundle aggregates independently versioned release modules and makes no
compatibility claim of its own. A bundle commit SHA is exact, immutable,
auditable, and already understood by Git. Human-readable source SemVer stays in
provenance. `main` is the install channel used by:

```bash
bunx skills@latest add giacomoguidotto/skills -y -g
```

Installed skills still update only when the user explicitly runs the skills CLI
or asks an agent to upgrade them.
