<p align="center">
  <img src="assets/logo.svg" alt="Knowledge Bank Infrastructure logo" width="160">
</p>

<h1 align="center">Knowledge Bank Infrastructure</h1>

<p align="center">
  <strong>Infrastructure-as-Code for a personal agent operating system.</strong><br>
  <sub>Your knowledge stays where you work. Only the agent protocol lives in Git.</sub>
</p>

<p align="center">
  <a href="https://github.com/giacomoguidotto/kb-infra/actions"><img src="https://github.com/giacomoguidotto/kb-infra/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/giacomoguidotto/kb-infra/releases"><img src="https://img.shields.io/github/v/release/giacomoguidotto/kb-infra?sort=semver" alt="Release"></a>
  <a href="https://github.com/giacomoguidotto/kb-infra/blob/main/LICENSE"><img src="https://img.shields.io/github/license/giacomoguidotto/kb-infra" alt="License"></a>
</p>

<br>

AI agents are only as useful as the context they can reach — and every local copy of that context goes stale. **Knowledge Bank Infrastructure** keeps the boundary sharp: your knowledge stays in the provider you already use, and this repo holds only the *protocol* your agents follow to read it, write to it behind approval, and run scheduled work against it. Nothing here runs — like Terraform for a cloud, it's the declarative source that *materializes* into live systems. Fork it, run one command, and your agents are wired to your knowledge without ever mirroring it.

<p align="center">
  <img src="assets/diagram.png" alt="How Knowledge Bank Infrastructure fits together" width="820">
</p>

<p align="center">
  <sub>The provider is the memory · the runtime runs the automations · this repo is the spec.</sub>
</p>

## Install

1. Fork and clone this repo.
2. Open your favorite agent in the repo and run:

```sh
/setup-kb-infra
```

This connects your Knowledge Bank provider, collects your personal **bindings** into a gitignored file, installs the skills, and stands up the automations. Your knowledge never enters the repo — only the generic spec does.

## What's Inside

**Skills** — install into any agent that follows the `SKILL.md` standard:

- **`/lookup`** — read-only retrieval from your Knowledge Bank.
- **`/capture`** — writes, always behind an approval draft (below).
- **`/setup-kb-infra`** — materializes the whole thing on your machine.

**Automations** — generic prompts in [`docs/automations/`](docs/automations/), scheduled by your runtime and all rooted in `/lookup`: knowledge harvest, social drafts, portfolio sweeps, and job-hunt audits. Each proposes work; none writes without approval.

Every write goes through a reviewable draft first — the exact property and body diffs, plus the evidence read — and waits for your explicit approval:

![Example approval draft](assets/example-draft.png)

<sub>Mock data. Nothing is written until you approve the exact draft.</sub>

## Contributing

Free and open source under the [MIT License](LICENSE). Agents should start at [AGENTS.md](AGENTS.md); see [CONTRIBUTING.md](.github/CONTRIBUTING.md) to get involved.
