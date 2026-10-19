"""Offline sanity checks for the public integration repository."""

import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/mlreferee"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    try:
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        require(market["name"] == "mlreferee", "catalog identity")
        require(market["plugins"][0]["source"] == "./plugins/mlreferee", "plugin path")
        require(market["plugins"][0]["name"] == "mlreferee", "catalog plugin name")
        manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())
        require(manifest["name"] == "mlreferee", "plugin identity")
        require(manifest["license"] == "MIT", "integration license")
        require(bool(re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])), "plugin version")
        require(json.loads((PLUGIN / ".mcp.json").read_text()) == {"mcpServers": {
            "mlreferee": {"type": "http", "url": "https://api.mlreferee.com"}}}, "MCP config")
        skill = (PLUGIN / "skills/referee/SKILL.md").read_text()
        require(skill.startswith("---\nname: referee\n") and "\ndescription: " in skill,
                "skill metadata")
        require("download_audit_result" not in skill, "pending tool must not enter this release")
        require((ROOT / "LICENSE").read_bytes() == (PLUGIN / "LICENSE").read_bytes(), "license parity")
        example = ROOT / "examples/synthetic-regression"
        rows = list(csv.DictReader(io.StringIO((example / "example.csv").read_text())))
        require(len(rows) == 400, "synthetic fixture row count")
        require(set(rows[0]) == {"observation_time", "label_available_time", "entity",
                                "baseline", "candidate", "outcome"}, "synthetic columns")
        contract = json.loads((example / "contract.json").read_text())
        require(contract["baseline"] == ["baseline"] and contract["candidates"] == ["candidate"],
                "synthetic contract")
        require(contract["observation_time"] != contract["label_available_time"], "timing roles")
        secret = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
                            r"\b(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9_]{20,}")
        # Local practice data is intentionally ignored, but force-added files
        # must never bypass the publication check.
        tracked = subprocess.check_output(
            ["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
        require(not any(name.startswith(("data/", "outputs/")) for name in tracked),
                "runtime data or outputs must not be tracked")
        for path in ROOT.rglob("*"):
            parts = path.relative_to(ROOT).parts
            if parts[0] in {"data", "outputs"}:
                continue
            if any(part in {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv"}
                   for part in parts):
                continue
            require(not path.is_symlink(), "symlink is not allowed")
            if not path.is_file():
                continue
            require(path.suffix.lower() not in {".mp4", ".mov", ".webm", ".db", ".pem", ".key"},
                    "private or large artifact type")
            require(not path.name.startswith(".env") or path.name == ".env.example", "environment file")
            require(path.stat().st_size <= 5 * 1024 * 1024, "oversized public file")
            if path.suffix != ".png":
                try:
                    text = path.read_text()
                except UnicodeError:
                    raise ValueError("unexpected binary file") from None
                require(not secret.search(text), "credential-like content")
        # The hashing helper must use original bytes, not reserialized JSON.
        spec = importlib.util.spec_from_file_location(
            "public_report_hash", ROOT / "examples/report-integrity/hash_report.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            original = '{"report":"Synthetic café"}'.encode("utf-8")
            path.write_bytes(original)
            result = module.hash_report(path, True)
            require(result["sha256"] == hashlib.sha256(original).hexdigest(), "JSON byte hash")
            require(result["text_sha256"] == hashlib.sha256("Synthetic café".encode()).hexdigest(),
                    "text byte hash")
            path.write_bytes(original + b"\n")
            require(module.hash_report(path)["sha256"] != result["sha256"], "negative control")
    except (ValueError, KeyError, OSError, IndexError, subprocess.CalledProcessError):
        print("Public repository checks failed; review manifests, fixtures and staged files.")
        return 1
    print("Public repository checks passed. No network, authentication or evaluation was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
