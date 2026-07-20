# Prototype: Agentic OS repository and release contract

This throwaway prototype asks whether a self-contained release-module layout can
make Agentic OS installable without a runtime, a required Agentic OS checkout, or
a synchronized constellation release manifest. It exercises the proposed source
and installed paths against normal releases, internal-only changes, the
fork-owned Career System setup skill, and Knowledge System interface changes.

Run it with:

```bash
bash prototypes/agentic-os-repository-contract/run.sh
```

The prototype is not an implementation. Its candidate tree and release outcomes
exist only to make the design easy to challenge before issue #48 is resolved.

## Locked decision

Public skill directories are self-contained release modules. In particular,
`setup-agentic-os` carries the fixed, version-free topology and the automation
definitions it materializes. An installed public skill never needs an Agentic OS
checkout, a synchronized constellation manifest, or a hidden latest-release fetch.
Internal artifacts remain committed source and stay outside distribution.

The canonical `knowledge-system-interface/v1` support package lives under
`knowledge-system/skills/public/setup-knowledge-system/resources/`. Setup installs
one data-only copy at `<harness-skill-root>/knowledge-system-interface/v1/` for
`lookup` and `capture` to consume, and reconciles that installed tree by content.

The Agentic OS source tree has one compact constellation document, one root
glossary, explicit public and internal skill trees, and no duplicate public
automation tree. `/setup-agentic-os` owns the fixed repository contract and the
automation definitions it materializes. Each automation keeps its definition,
minimal Knowledge Request, and Knowledge Mandate together. Public integration
skills keep their mapper and cross-system procedure inside their own release
module. Internal automations remain under `automations/internal/` for explicit
repo-native installation.

The release contract follows the canonical `build` KB convention. Every commit
uses Conventional Commits. In a release-enabled repository, `fix:` triggers a
patch, `feat:` triggers a minor, and `feat!:`, `fix!:`, or `BREAKING CHANGE:`
triggers a major. Non-releasing types such as `docs:`, `chore:`, `refactor:`,
`ci:`, and `test:` do not publish. Public versus internal controls distribution,
not versioning, so a release-triggering internal change still releases its owner.
