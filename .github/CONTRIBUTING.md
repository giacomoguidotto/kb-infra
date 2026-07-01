# Contributing

Thanks for your interest in Knowledge Bank Infrastructure! Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before getting started.

Knowledge Bank Infrastructure is my source-of-record for a provider-backed knowledge system, so contributions are accepted on a limited basis.

## What We Accept

- Bug fixes for repo-owned docs, skills, templates, and validation rules.
- Documentation improvements that make agent workflows clearer or safer.
- Security and export-safety fixes.
- Small workflow improvements discussed in an issue first.

## What We Do Not Accept

- Pull requests that include private KB content, broad personal context, or generated private artifacts.
- Unsolicited workflow rewrites without an issue and maintainer agreement.
- Runtime infrastructure that turns Knowledge Bank Infrastructure into the source of truth or a background process.
- Refactoring for its own sake.

## Setup

1. Fork and clone the repo.
2. Read [AGENTS.md](../AGENTS.md) for the source-of-record framing, the tool belt, and the export-safety rules, and [CONTEXT.md](../CONTEXT.md) for vocabulary.
3. Make a focused change.
4. Before pushing, run:

    ```sh
    bash scripts/check.sh
    git diff --check
    ```

## Workflow

1. Open an issue first for anything larger than a typo or small docs fix.
2. Fork the repository and create a branch from `main`.
3. Keep the scope small and focused on one concern.
4. Open a pull request against `main` and reference the issue it addresses.

## Tooling

- Nothing in this repo runs; it is a spec. There is no app build step.
- `scripts/check.sh` validates the spec: no personal coupling or absolute paths,
  no retired terms, skill frontmatter present, every automation references the
  preamble, and internal links resolve. CI runs it on every push and PR.
- `git diff --check` guards patch whitespace.

## Conventions

- Branch names: `feat/`, `fix/`, `docs/`, `refactor/`, `test/`, `chore/`.
- Commits: [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) such as `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, and `chore:`.
- Use Knowledge Bank Infrastructure's domain terms from [CONTEXT.md](../CONTEXT.md).
- Keep public artifacts routing-safe. Do not include private KB material unless the maintainer explicitly approves the exact export.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](../LICENSE).
