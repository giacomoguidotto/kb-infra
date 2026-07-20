#!/usr/bin/env bash

# Pure presentation model for the repository-contract prototype. Functions emit
# deterministic text and do not read input, write files, or mutate external state.

prototype_tree() {
  cat <<'EOF'
agentic-os/
status: repository layout locked
├── AGENTS.md
├── CONTEXT.md                         # system-wide vocabulary only
├── README.md
├── docs/
│   ├── adr/                           # hard-to-reverse Agentic OS decisions
│   └── constellation.md               # low-resolution map and owner links only
├── skills/
│   ├── public/                        # sole Distribution Bundle export surface
│   │   ├── setup-agentic-os/
│   │   │   ├── SKILL.md               # /setup-agentic-os interface
│   │   │   └── resources/
│   │   │       ├── repository-contract.yml  # fixed repos/branches, no versions
│   │   │       └── automations/
│   │   │           └── <automation>/
│   │   │               ├── definition.md
│   │   │               ├── knowledge-request.yml
│   │   │               └── knowledge-mandate.yml
│   │   ├── domain-reconnaissance/
│   │   ├── post/
│   │   ├── tweet/                     # small preset over /post
│   │   └── career-integration/
│   │       ├── SKILL.md
│   │       └── resources/
│   │           ├── mapper/            # Knowledge to Career Profile Snapshot
│   │           └── schemas/           # scout and pursue run results
│   └── internal/                      # committed, public-safe, not distributed
│       └── setup-project/
├── automations/
│   └── internal/
│       └── repo-pr-ci-repair-sweep/   # explicit local installation only
├── local/
│   └── installation.example.yml       # three roots; live file is gitignored
└── scripts/check.sh

knowledge-system/
└── skills/public/
    ├── lookup/
    ├── capture/
    └── setup-knowledge-system/
        └── resources/knowledge-system-interface/v1/
            ├── schemas/               # request, snapshot, mandate, health
            └── endpoint-registry/     # canonical declarative registry source

career-ops fork/
└── skills/public/setup-career-system/ # sole positively allowed fork export
EOF
}

prototype_installed_tree() {
  cat <<'EOF'
<harness-skill-root>/
├── setup-agentic-os/                  # verbatim public skill and resources
├── lookup/
├── capture/
├── setup-knowledge-system/
├── setup-mastery-system/
├── setup-career-system/
└── knowledge-system-interface/v1/     # setup-managed shared support package
    ├── schemas/
    └── endpoint-registry/

The interface is installed once per harness, next to the skills that consume it.
/lookup and /capture resolve it relative to their harness skill root.
/setup-knowledge-system hashes and reconciles the whole installed support package.
EOF
}

prototype_release_contract() {
  cat <<'EOF'
status: release contract locked
canonical convention: every commit follows Conventional Commits
release applicability: SemVer is mandatory because these repositories publish distributed skills

commit: fix:
owner release: patch

commit: feat:
owner release: minor

commit: feat!:, fix!:, or BREAKING CHANGE:
owner release: major

commit: docs:, chore:, refactor:, ci:, or test:
owner release: none under the repository release automation

rule: export disposition never chooses the release type
example: a fix: to skills/internal still triggers a patch release even though the bundle excludes it
rule: before committing a release-triggering type, inspect the repository release automation and confirm the intended release level

distribution eligibility:
- Agentic OS, Knowledge System, and Mastery System export released skills/public/*
- the Career Ops fork exports only released skills/public/setup-career-system
- source releases are immutable evidence, never synchronized compatibility pins
- setup validates supported interface majors live and blocks only affected capabilities
- trigger, concurrency, rollback, and bundle-version mechanics remain in issue #43
EOF
}

prototype_scenario() {
  case "$1" in
    agentic-release)
      cat <<'EOF'
event: Agentic OS publishes an immutable release
source: agentic-os skills/public/*
bundle: full rebuild copies every public skill directory verbatim
automations: setup-agentic-os/resources/automations travels with the setup skill
local install: unchanged until the user explicitly upgrades installed skills
result: no checkout lookup, latest-release fetch, or subsystem release pin
EOF
      ;;
    registry-change)
      cat <<'EOF'
event: an Endpoint Registry role definition changes compatibly
source: knowledge-system/skills/public/setup-knowledge-system/resources/knowledge-system-interface/v1/endpoint-registry
status: source and installed paths locked
release: Knowledge System publishes its independently chosen release
bundle: full rebuild copies the released /setup-knowledge-system skill verbatim
setup: /setup-knowledge-system detects the registry hash and binding impact
runtime: affected Snapshot Tokens become invalid through the registry revision
result: interface major stays v1; no Agentic OS file copies Knowledge rules
EOF
      ;;
    career-release)
      cat <<'EOF'
event: giacomoguidotto/career-ops releases setup-career-system
source: career-ops/skills/public/setup-career-system only
bundle: positive allowlist copies that one directory verbatim
excluded: .agents/skills, operational skills, and santifer/career-ops releases
agentic-os: validates the live Career System interface at setup time
result: fork ownership is preserved without absorbing Career Ops behavior
EOF
      ;;
    internal-change)
      cat <<'EOF'
event: an internal skill or Repo PR CI Repair Sweep changes
release: its Conventional Commit type determines whether the repository publishes
bundle: skills/internal and automations/internal are never scanned
local install: changed only through an explicit repo-native installation action
result: internal remains an export disposition, not a release type or secrecy boundary
EOF
      ;;
    breaking-interface)
      cat <<'EOF'
event: a System makes an incompatible interface change
release: the owning System publishes a major release
agentic-os: keeps its independent release line and declares supported interface majors
setup: validates the live combination and blocks only affected integrations
bundle: provenance records source releases as evidence, never as a compatibility lock
result: no constellation-wide release, version matrix, or synchronized manifest
EOF
      ;;
    invariants)
      cat <<'EOF'
invariant: public skills are self-contained release modules
status: locked
invariant: skills/public is the only normal first-party bundle export surface
invariant: the Career Ops setup skill is one explicit fork-owned exception
invariant: internal artifacts are committed and public-safe but not distributed
invariant: setup topology commits repository identities and branches, never versions
invariant: each repository releases independently
invariant: local upgrades are explicit
invariant: no runtime service, shared database, release manifest, or hidden latest fetch
EOF
      ;;
    release-contract)
      prototype_release_contract
      ;;
    *)
      return 1
      ;;
  esac
}
