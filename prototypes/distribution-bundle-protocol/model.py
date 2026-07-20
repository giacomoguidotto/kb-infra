#!/usr/bin/env python3
"""In-memory state model for the throwaway Distribution Bundle prototype."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


PROTOTYPE_DIR = Path(__file__).resolve().parent
REGISTRY = json.loads((PROTOTYPE_DIR / "protocol" / "exports.json").read_text())
AUTHORIZED_ACTOR = "agentic-os-distribution-trigger[bot]"


@dataclass(frozen=True)
class Release:
    repository: str
    release_id: int
    tag: str
    commit: str
    immutable: bool
    stable: bool
    skills: dict[str, tuple[str, str]]


@dataclass(frozen=True)
class Revision:
    commit: str
    parent: str
    skills: dict[str, str]
    provenance: dict[str, object]


class ProtocolError(RuntimeError):
    pass


class BundleModel:
    def __init__(self) -> None:
        self.registry = {
            item["repository"]: tuple(item["exports"])
            for item in REGISTRY["sources"]
        }
        self.releases: dict[str, list[Release]] = {
            repository: [] for repository in self.registry
        }
        self.pending = False
        self.history: list[Revision] = []
        self.log: list[str] = []
        self._release_id = 1000
        self._commit_nonce = 0

    @property
    def active(self) -> Revision | None:
        return self.history[-1] if self.history else None

    def publish_source(
        self,
        repository: str,
        tag: str,
        skills: dict[str, tuple[str, str]],
        *,
        immutable: bool = True,
        stable: bool = True,
    ) -> Release:
        self._release_id += 1
        digest = hashlib.sha256(f"{repository}:{tag}".encode()).hexdigest()[:12]
        release = Release(
            repository=repository,
            release_id=self._release_id,
            tag=tag,
            commit=digest,
            immutable=immutable,
            stable=stable,
            skills=skills,
        )
        self.releases[repository].append(release)
        self.log.append(f"source release: {repository}@{tag}")
        return release

    def dispatch(self, actor: str, hinted_repository: str, hinted_tag: str) -> bool:
        if actor != AUTHORIZED_ACTOR or hinted_repository not in self.registry:
            self.log.append(
                f"dispatch rejected: actor={actor} hint={hinted_repository}@{hinted_tag}"
            )
            return False
        self.pending = True
        self.log.append(
            f"wake-up accepted: {hinted_repository}@{hinted_tag}; payload is not input"
        )
        return True

    def reconcile(self) -> str:
        selected: dict[str, Release] = {}
        candidate: dict[str, tuple[str, str, str, str]] = {}

        for repository, patterns in self.registry.items():
            stable = [release for release in self.releases[repository] if release.stable]
            if not stable:
                raise ProtocolError(f"no stable release: {repository}")
            release = stable[-1]
            if not release.immutable:
                raise ProtocolError(f"mutable release blocked: {repository}@{release.tag}")
            selected[repository] = release

            for path, (declared_name, content) in sorted(release.skills.items()):
                if not any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns):
                    continue
                directory_name = Path(path).name
                if declared_name != directory_name:
                    raise ProtocolError(
                        f"invalid name: {path} declares {declared_name}"
                    )
                if declared_name in candidate:
                    owner = candidate[declared_name][0]
                    raise ProtocolError(
                        f"name collision: {declared_name} from {owner} and {repository}"
                    )
                candidate[declared_name] = (
                    repository,
                    release.tag,
                    path,
                    content,
                )

        skills = {
            name: item[3]
            for name, item in sorted(candidate.items())
        }
        provenance_sources = []
        for repository, release in sorted(selected.items()):
            exports = []
            for name, item in sorted(candidate.items()):
                if item[0] != repository:
                    continue
                exports.append(
                    {
                        "name": name,
                        "path": item[2],
                        "tree_sha256": hashlib.sha256(item[3].encode()).hexdigest(),
                    }
                )
            archive_material = "\n".join(
                f"{path}:{declared}:{content}"
                for path, (declared, content) in sorted(release.skills.items())
            )
            provenance_sources.append(
                {
                    "repository": repository,
                    "release_id": release.release_id,
                    "tag": release.tag,
                    "commit": release.commit,
                    "archive_sha256": hashlib.sha256(
                        archive_material.encode()
                    ).hexdigest(),
                    "exports": exports,
                }
            )

        provenance = {
            "schema": "distribution-provenance/v1",
            "sources": provenance_sources,
        }
        if self.active and self.active.skills == skills and self.active.provenance == provenance:
            self.log.append("reconcile: exact state already active; no-op")
            return "no-op"

        revision = self._new_revision(skills, provenance)
        self.history.append(revision)
        self.log.append(f"published atomically: {revision.commit}")
        return revision.commit

    def run_pending(self) -> str:
        if not self.pending:
            self.log.append("runner: no pending wake-up")
            return "no-op"
        self.pending = False
        return self.reconcile()

    def rollback(self, target_commit: str) -> str:
        target = next(
            (revision for revision in self.history if revision.commit == target_commit),
            None,
        )
        if target is None:
            raise ProtocolError(f"unknown bundle commit: {target_commit}")
        revision = self._new_revision(target.skills, target.provenance)
        self.history.append(revision)
        self.log.append(
            f"rollback: restored {target_commit} as new commit {revision.commit}"
        )
        return revision.commit

    def _new_revision(
        self, skills: dict[str, str], provenance: dict[str, object]
    ) -> Revision:
        self._commit_nonce += 1
        parent = self.active.commit if self.active else "root"
        tree = json.dumps(
            {"skills": skills, "provenance": provenance},
            sort_keys=True,
            separators=(",", ":"),
        )
        commit = hashlib.sha256(
            f"{parent}:{self._commit_nonce}:{tree}".encode()
        ).hexdigest()[:12]
        return Revision(commit=commit, parent=parent, skills=skills, provenance=provenance)

    def render(self) -> str:
        active = self.active
        if active is None:
            return "active bundle: none\npending reconciliation: " + str(self.pending).lower()
        source_lines = [
            f"  {item['repository']}@{item['tag']} ({item['commit']})"
            for item in active.provenance["sources"]
        ]
        skill_lines = [f"  {name}" for name in active.skills]
        return "\n".join(
            [
                f"active bundle commit: {active.commit}",
                f"parent: {active.parent}",
                f"pending reconciliation: {str(self.pending).lower()}",
                "source provenance:",
                *source_lines,
                "published skills:",
                *skill_lines,
            ]
        )


def skill(repository: str, name: str, version: str) -> tuple[str, str]:
    return name, f"{repository}:{name}:{version}"


def seed() -> BundleModel:
    model = BundleModel()
    model.publish_source(
        "giacomoguidotto/agentic-os",
        "v0.1.0",
        {
            "skills/public/setup-agentic-os": skill("agentic-os", "setup-agentic-os", "1"),
            "skills/public/career-integration": skill("agentic-os", "career-integration", "1"),
            "skills/internal/setup-project": skill("agentic-os", "setup-project", "1"),
        },
    )
    model.publish_source(
        "giacomoguidotto/knowledge-system",
        "v0.9.0",
        {
            "skills/public/lookup": skill("knowledge-system", "lookup", "1"),
            "skills/public/capture": skill("knowledge-system", "capture", "1"),
            "skills/public/setup-knowledge-system": skill(
                "knowledge-system", "setup-knowledge-system", "1"
            ),
            "skills/internal/get-knowledge": skill(
                "knowledge-system", "get-knowledge", "1"
            ),
        },
    )
    model.publish_source(
        "giacomoguidotto/mastery-system",
        "v0.2.0",
        {
            "skills/public/setup-mastery-system": skill(
                "mastery-system", "setup-mastery-system", "1"
            )
        },
    )
    model.publish_source(
        "giacomoguidotto/career-ops",
        "v2.4.0-fork.1",
        {
            "skills/public/setup-career-system": skill(
                "career-ops", "setup-career-system", "1"
            ),
            "skills/public/job-scout": skill("career-ops", "job-scout", "1"),
            ".agents/skills/career-ops": skill("career-ops", "career-ops", "1"),
        },
    )
    model.reconcile()
    model.log.clear()
    return model


def scenario_allowlist() -> tuple[BundleModel, str]:
    model = seed()
    assert "setup-career-system" in model.active.skills
    assert "job-scout" not in model.active.skills
    assert "career-ops" not in model.active.skills
    return model, "The fork contributes only setup-career-system; internal and operational surfaces stay out."


def scenario_concurrent() -> tuple[BundleModel, str]:
    model = seed()
    model.publish_source(
        "giacomoguidotto/agentic-os",
        "v0.2.0",
        {
            "skills/public/setup-agentic-os": skill("agentic-os", "setup-agentic-os", "2"),
            "skills/public/career-integration": skill("agentic-os", "career-integration", "2"),
            "skills/internal/setup-project": skill("agentic-os", "setup-project", "2"),
        },
    )
    model.dispatch(AUTHORIZED_ACTOR, "giacomoguidotto/agentic-os", "v0.2.0")
    model.publish_source(
        "giacomoguidotto/mastery-system",
        "v0.3.0",
        {
            "skills/public/setup-mastery-system": skill(
                "mastery-system", "setup-mastery-system", "2"
            ),
            "skills/public/mastery-integration": skill(
                "mastery-system", "mastery-integration", "1"
            ),
        },
    )
    model.dispatch(AUTHORIZED_ACTOR, "giacomoguidotto/mastery-system", "v0.3.0")
    model.run_pending()
    tags = {item["repository"]: item["tag"] for item in model.active.provenance["sources"]}
    assert tags["giacomoguidotto/agentic-os"] == "v0.2.0"
    assert tags["giacomoguidotto/mastery-system"] == "v0.3.0"
    return model, "Coalesced notifications still publish both latest releases in one full rebuild."


def scenario_removal() -> tuple[BundleModel, str]:
    model = seed()
    model.publish_source(
        "giacomoguidotto/knowledge-system",
        "v0.10.0",
        {
            "skills/public/lookup": skill("knowledge-system", "lookup", "2"),
            "skills/public/setup-knowledge-system": skill(
                "knowledge-system", "setup-knowledge-system", "2"
            ),
        },
    )
    model.dispatch(AUTHORIZED_ACTOR, "giacomoguidotto/knowledge-system", "v0.10.0")
    model.run_pending()
    assert "capture" not in model.active.skills
    return model, "A new immutable source release omitting capture removes it during the full rebuild."


def scenario_collision() -> tuple[BundleModel, str]:
    model = seed()
    previous = model.active.commit
    model.publish_source(
        "giacomoguidotto/mastery-system",
        "v0.3.0",
        {
            "skills/public/setup-mastery-system": skill(
                "mastery-system", "setup-mastery-system", "2"
            ),
            "skills/public/lookup": skill("mastery-system", "lookup", "1"),
        },
    )
    model.dispatch(AUTHORIZED_ACTOR, "giacomoguidotto/mastery-system", "v0.3.0")
    try:
        model.run_pending()
    except ProtocolError as error:
        model.log.append(f"publication failed closed: {error}")
    assert model.active.commit == previous
    return model, "A duplicate skill name fails validation before publication; the active bundle is unchanged."


def scenario_unauthorized() -> tuple[BundleModel, str]:
    model = seed()
    previous = model.active.commit
    accepted = model.dispatch(
        "mallory", "santifer/career-ops", "v99.0.0"
    )
    assert not accepted
    assert not model.pending
    assert model.active.commit == previous
    return model, "An unauthorized or unlisted dispatch cannot select content or schedule publication."


def scenario_mutable() -> tuple[BundleModel, str]:
    model = seed()
    previous = model.active.commit
    model.publish_source(
        "giacomoguidotto/agentic-os",
        "v0.2.0",
        {
            "skills/public/setup-agentic-os": skill("agentic-os", "setup-agentic-os", "2")
        },
        immutable=False,
    )
    model.dispatch(AUTHORIZED_ACTOR, "giacomoguidotto/agentic-os", "v0.2.0")
    try:
        model.run_pending()
    except ProtocolError as error:
        model.log.append(f"publication failed closed: {error}")
    assert model.active.commit == previous
    return model, "A latest source release without immutable-release enforcement blocks the rebuild."


def scenario_rollback() -> tuple[BundleModel, str]:
    model = seed()
    target = model.active.commit
    target_skills = dict(model.active.skills)
    model.publish_source(
        "giacomoguidotto/agentic-os",
        "v0.2.0",
        {
            "skills/public/setup-agentic-os": skill("agentic-os", "setup-agentic-os", "2")
        },
    )
    model.dispatch(AUTHORIZED_ACTOR, "giacomoguidotto/agentic-os", "v0.2.0")
    changed = model.run_pending()
    restored = model.rollback(target)
    assert restored != target
    assert restored != changed
    assert model.active.skills == target_skills
    assert model.active.parent == changed
    return model, "Rollback restores a prior snapshot as a new forward commit without rewriting history."


def scenario_noop() -> tuple[BundleModel, str]:
    model = seed()
    previous = model.active.commit
    outcome = model.reconcile()
    assert outcome == "no-op"
    assert model.active.commit == previous
    return model, "Deterministic provenance makes an unchanged scheduled rebuild a true no-op."


SCENARIOS: dict[str, tuple[str, Callable[[], tuple[BundleModel, str]]]] = {
    "allowlist": ("Career fork positive allowlist", scenario_allowlist),
    "concurrent": ("Concurrent release notifications", scenario_concurrent),
    "removal": ("Published skill removal", scenario_removal),
    "collision": ("Cross-repository name collision", scenario_collision),
    "unauthorized": ("Unauthorized dispatch", scenario_unauthorized),
    "mutable": ("Mutable source release", scenario_mutable),
    "rollback": ("Forward-only rollback", scenario_rollback),
    "noop": ("Scheduled no-op reconciliation", scenario_noop),
}


def render_scenario(name: str) -> str:
    title, scenario = SCENARIOS[name]
    model, verdict = scenario()
    log = "\n".join(f"  {line}" for line in model.log) or "  none"
    return "\n".join(
        [
            title,
            "=" * len(title),
            "",
            "Transitions:",
            log,
            "",
            "Full active state:",
            model.render(),
            "",
            f"Verdict: {verdict}",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", nargs="?", choices=SCENARIOS)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    names = list(SCENARIOS) if args.all else [args.scenario or "allowlist"]
    for index, name in enumerate(names):
        if index:
            print("\n" + "-" * 72 + "\n")
        print(render_scenario(name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
