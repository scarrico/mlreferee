# Hash an original report locally

This utility needs Python 3. It uses only the standard library and makes no
network request. It does not upload a report, use credentials or spend credits.

First obtain the original `report.json` through an authorized download supported
by your client. This utility does not add a download tool to a connection. The
pending agent download tool is not assumed to be deployed or approved.

```sh
python3 examples/report-integrity/hash_report.py /path/to/report.json --include-text
```

The output contains the computed SHA-256 and byte count for the unchanged file.
With `--include-text`, it also hashes the parsed top-level `report` string's
UTF-8 bytes without adding a newline. Feed the locally computed candidate digest
to the discovered `verify_audit_report` tool with the correct audit ID and
`representation: result_json` or `representation: report_text`, respectively.

Do not use an API/MCP envelope, pretty-print or reserialize the JSON, or copy
the expected receipt digest as the candidate. This script only computes hashes:
it cannot authenticate a report by itself. A matching service receipt establishes
byte consistency, not correctness or safety. Keep actual reports and receipts
private; never commit them to this public examples directory.
