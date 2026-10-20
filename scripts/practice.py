"""Run local practice checks without network access, authentication or uploads."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(*args, capture=False):
    return subprocess.run([sys.executable, *args], cwd=ROOT, check=True,
                          text=True, capture_output=capture)


def main():
    print("1. Check the 400-row synthetic input (not a hosted evaluation).", flush=True)
    run("scripts/check_example.py", "examples/synthetic-regression/example.csv",
        "examples/synthetic-regression/contract.json")
    print("2. Test preparation, timing and reserved-data boundaries offline.", flush=True)
    run("-m", "unittest", "discover", "-s", "tests", "-v")
    print("3. Demonstrate report fingerprints using an explicitly synthetic artifact.", flush=True)
    with tempfile.TemporaryDirectory(prefix="mlreferee-practice-") as directory:
        path = Path(directory) / "synthetic-not-issued.json"
        raw = b'{"report":"Practice only. Not an issued Referee report."}'
        path.write_bytes(raw)
        first = json.loads(run("examples/report-integrity/hash_report.py", str(path),
                               "--include-text", capture=True).stdout)
        if first["sha256"] != hashlib.sha256(raw).hexdigest():
            raise ValueError("Original-byte fingerprint mismatch")
        path.write_bytes(raw + b"\n")
        changed = json.loads(run("examples/report-integrity/hash_report.py", str(path),
                                 "--include-text", capture=True).stdout)
        if first["sha256"] == changed["sha256"]:
            raise ValueError("Changed bytes were not detected")
        if first["text_sha256"] != changed["text_sha256"]:
            raise ValueError("Unchanged report text unexpectedly changed fingerprint")
    print("PASS: local exercises complete; temporary synthetic artifact removed.")
    print("No service sign-in, preflight, evaluation or report verification was performed.")
    print("Next: examples/bike-demand/README.md and docs/coding-agents.md")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Practice check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
