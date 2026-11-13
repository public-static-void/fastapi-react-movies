"""Dependency invariant tests for the lock-file single source of truth.

The poetry lock file is the only committed artifact that pins Python
package versions and hashes. These tests keep CI and the Docker build
deriving their pip inputs from the lock at use time, keep the poetry
toolchain exactly pinned, and keep Dependabot scoped to manifest paths.
"""

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"
DEPENDABOT_CONFIG = REPO_ROOT / ".github" / "dependabot.yml"
DOCKERFILE = REPO_ROOT / "backend" / "movies_backend" / "Dockerfile"

BACKEND_WORKFLOWS = (
    "backend-lint.yml",
    "backend-test.yml",
    "release.yml",
)

PINNED_EXPORT_BASENAME = re.compile(
    r"(requirements|constraints)[^/]*\.txt$"
)
EXPORT_GUARD_REMNANT = re.compile(
    r"Export-diff guard|diff requirements|tmp_export"
)
POETRY_INSTALL_LINE = re.compile(r"pip install.*poetry")
HASHLESS_FLAG = re.compile(r"--without-hashes|--generate-hashes")


def tracked_files():
    """List every path tracked by git at the repository root."""
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        "git ls-files failed: " + result.stderr.strip()
    )
    return result.stdout.splitlines()


def workflow_text(name):
    """Return the full text of a backend workflow file."""
    path = WORKFLOWS_DIR / name
    assert path.is_file(), f"missing workflow: {path.name}"
    return path.read_text(encoding="utf-8")


def workflow_sources():
    """Return every workflow file plus the backend Dockerfile."""
    paths = sorted(WORKFLOWS_DIR.glob("*.yml"))
    return paths + [DOCKERFILE]


def dependabot_entries():
    """Parse dependabot.yml into entry dicts, without PyYAML."""
    assert DEPENDABOT_CONFIG.is_file(), "missing .github/dependabot.yml"
    content = DEPENDABOT_CONFIG.read_text(encoding="utf-8")
    entries = []
    current = None
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("package-ecosystem:"):
            value = stripped.split(":", 1)[1].strip().strip('"')
            current = {
                "ecosystem": value,
                "directory": None,
                "interval": False,
                "groups": False,
            }
            entries.append(current)
        elif current is None:
            continue
        elif "directory:" in stripped:
            value = stripped.split(":", 1)[1].strip().strip('"')
            current["directory"] = value
        elif "interval:" in stripped:
            current["interval"] = True
        elif "groups:" in stripped:
            current["groups"] = True
    return content, entries


def test_no_committed_requirements_or_constraints_files():
    """Version control carries no derived pip requirement pins."""
    offenders = [
        path
        for path in tracked_files()
        if PINNED_EXPORT_BASENAME.match(path.rsplit("/", 1)[-1])
    ]
    assert not offenders, (
        "derived exports must not be committed: "
        + ", ".join(offenders)
    )


def test_backend_workflows_derive_dependencies_from_lock():
    """Each backend workflow checks the lock and exports at job time."""
    for name in BACKEND_WORKFLOWS:
        text = workflow_text(name)
        assert "poetry check --lock" in text, (
            f"{name}: missing 'poetry check --lock'"
        )
        assert "poetry export" in text, (
            f"{name}: missing 'poetry export'"
        )


def test_backend_workflows_ignore_deleted_requirements_files():
    """No backend workflow reads the removed requirements files."""
    forbidden = (
        "requirements-dev",
        "pip install -r requirements",
        "[ -f requirements-dev.txt ]",
    )
    for name in BACKEND_WORKFLOWS:
        text = workflow_text(name)
        for fragment in forbidden:
            assert fragment not in text, (
                f"{name}: references {fragment!r}"
            )


def test_no_export_byte_diffs_in_any_workflow():
    """No workflow compares a committed export with a fresh export."""
    for path in sorted(WORKFLOWS_DIR.glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        match = EXPORT_GUARD_REMNANT.search(text)
        assert match is None, (
            f"{path.name}: export-diff remnant {match.group(0)!r}"
        )


def test_dockerfile_derives_runtime_requirements_from_lock():
    """The image build exports from the lock, not a pinned file."""
    text = DOCKERFILE.read_text(encoding="utf-8")
    copy_lines = [
        line
        for line in text.splitlines()
        if line.strip().startswith("COPY")
    ]
    for line in copy_lines:
        assert "requirements.txt" not in line, (
            f"COPY of a committed export remains: {line.strip()}"
        )
    assert any("poetry.lock" in line for line in copy_lines), (
        "builder stage does not copy poetry.lock"
    )
    assert "poetry export" in text, "no export from the lock"
    assert "--only main" in text, "prod export must use --only main"
    assert re.search(r"pip install.*-r ", text), (
        "exported requirements are not installed"
    )


def test_poetry_toolchain_is_exactly_pinned():
    """Every install of poetry also pins the export plugin exactly."""
    for path in workflow_sources():
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if not POETRY_INSTALL_LINE.search(line):
                continue
            assert "poetry==" in line, (
                f"{path.name}: unpinned poetry: {line.strip()}"
            )
            assert "poetry-plugin-export==" in line, (
                f"{path.name}: unpinned plugin: {line.strip()}"
            )


def test_hash_verification_is_never_disabled():
    """No workflow or image build turns off pip hash checking."""
    for path in workflow_sources():
        text = path.read_text(encoding="utf-8")
        match = HASHLESS_FLAG.search(text)
        assert match is None, (
            f"{path.name}: forbidden flag {match.group(0)!r}"
        )


def test_dependabot_config_scopes_three_manifest_directories():
    """Dependabot watches each manifest directory on a schedule."""
    content, entries = dependabot_entries()
    assert re.search(r"^version:\s*2\s*$", content, re.M), (
        "dependabot.yml must declare version: 2"
    )
    expected = {
        ("pip", "/backend/movies_backend"),
        ("npm", "/frontend/movies_frontend"),
        ("github-actions", "/"),
    }
    actual = {(e["ecosystem"], e["directory"]) for e in entries}
    assert len(entries) == 3, f"expected 3 entries, found {len(entries)}"
    assert actual == expected, f"unexpected entry set: {actual}"
    for entry in entries:
        assert entry["interval"], (
            f"{entry['ecosystem']}: missing schedule interval"
        )
    pip_entries = [e for e in entries if e["ecosystem"] == "pip"]
    assert len(pip_entries) == 1, "expected exactly one pip entry"
    assert pip_entries[0]["groups"], "pip entry needs a groups rule"


def test_dependabot_config_avoids_forbidden_keys():
    """Config stays compatible with security updates: no filters."""
    assert DEPENDABOT_CONFIG.is_file(), "missing .github/dependabot.yml"
    content = DEPENDABOT_CONFIG.read_text(encoding="utf-8")
    for forbidden in (
        "target-branch",
        "allow:",
        "ignore:",
        "open-pull-requests-limit: 0",
        "requirements",
    ):
        assert forbidden not in content, (
            f"dependabot.yml must not contain {forbidden!r}"
        )
