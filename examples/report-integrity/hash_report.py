"""Compute candidate digests from an original local report; no network access."""

import argparse
import hashlib
import json
from pathlib import Path


def hash_report(path, include_text=False):
    raw = path.read_bytes()
    result = {"representation": "result_json", "sha256": hashlib.sha256(raw).hexdigest(),
              "bytes": len(raw)}
    if include_text:
        content = json.loads(raw)
        if not isinstance(content, dict) or not isinstance(content.get("report"), str):
            raise ValueError("Expected an original report with a top-level report string, not an envelope")
        text = content["report"].encode("utf-8")
        result.update(text_sha256=hashlib.sha256(text).hexdigest(), text_bytes=len(text))
    return result


def hash_report_text(path):
    """Hash exact saved UTF-8 report text without newline normalization."""
    raw = path.read_bytes()
    raw.decode("utf-8")  # Reject invalid UTF-8; never silently replace bytes.
    return {"representation": "report_text",
            "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--include-text", action="store_true")
    modes.add_argument("--text-file", action="store_true",
                       help="Hash an exact UTF-8 report-text file, not JSON")
    args = parser.parse_args()
    try:
        result = (hash_report_text(args.report) if args.text_file else
                  hash_report(args.report, args.include_text))
    except (OSError, ValueError):
        parser.exit(1, "Could not hash the report; check the path and selected JSON/UTF-8 format.\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
