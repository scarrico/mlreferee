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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--include-text", action="store_true")
    args = parser.parse_args()
    try:
        result = hash_report(args.report, args.include_text)
    except (OSError, ValueError):
        parser.exit(1, "Could not hash an original report file; check the path and JSON format.\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
