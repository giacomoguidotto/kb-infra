# Contributing

Thanks for your interest in Knowledge Bank Infrastructure! Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before getting started.

Knowledge Bank Infrastructure is Giacomo's local infrastructure for a Notion-first knowledge system, so contributions are accepted on a limited basis.

## What We Accept

- Bug fixes for repo-owned docs, skills, templates, and validation rules.
- Documentation improvements that make agent workflows clearer or safer.
- Security and export-safety fixes.
- Small workflow improvements discussed in an issue first.

## What We Do Not Accept

- Pull requests that include private Notion content, broad personal context, or generated private artifacts.
- Unsolicited workflow rewrites without an issue and maintainer agreement.
- Runtime infrastructure that turns Knowledge Bank Infrastructure into the source of truth or a background process.
- Refactoring for its own sake.

## Setup

1. Fork and clone the repo.
2. Read [agent navigation](../docs/agents/navigation.md) for the Notion-first source-of-truth, loading, export-safety, and validation rules.
3. Make a focused change.
4. Before pushing, run:

    ```sh
    git diff --check
    ```

## Workflow

1. Open an issue first for anything larger than a typo or small docs fix.
2. Fork the repository and create a branch from `main`.
3. Keep the scope small and focused on one concern.
4. Open a pull request against `main` and reference the issue it addresses.

## Tooling

- There is no app build step yet.
- `git diff --check` is the current required validation.
- Future generated artifact validators should be documented next to the artifact or workflow they validate.

## Conventions

- Branch names: `feat/`, `fix/`, `docs/`, `refactor/`, `test/`, `chore/`.
- Commits: [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) such as `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, and `chore:`.
- Use Knowledge Bank Infrastructure's domain terms from [CONTEXT.md](../CONTEXT.md).
- Keep public artifacts routing-safe. Do not include private Notion material unless Giacomo explicitly approves the exact export.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](../LICENSE).
