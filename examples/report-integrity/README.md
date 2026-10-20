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

## When only report text is available

If the live result returns `result.report`, save that exact string as UTF-8 in
a private text file, without adding a newline or changing line endings. Do not
copy rendered Markdown from a chat bubble: formatting, escaping and wrapping
can change its bytes. If your client cannot preserve the exact returned string,
say verification is unavailable rather than reconstructing a report.

```sh
python3 examples/report-integrity/hash_report.py /path/to/private/report.txt --text-file
```

Use the returned candidate digest with `representation: report_text` and the
matching audit's live `verify_audit_report` tool. Obtain the receipt separately
with `get_audit_receipt`. The local command performs no network verification.
It neither strips nor adds whitespace; a changed newline changes the hash.
This text path was used in the completed Codex synthetic workflow. On October 20,
the Copilot synthetic evaluation also used this exact `--text-file` command on
the saved report and received `digest_match` from the live service. This verifies
the report text, not an original JSON download.

If verification fails, check representation, audit identity, encoding and exact
bytes. Do not replace your computed digest with the receipt's expected digest
to obtain a match. Save artifacts before their returned expiry; completion does
not restart the retention clock. Deletion requires a separate explicit request.
