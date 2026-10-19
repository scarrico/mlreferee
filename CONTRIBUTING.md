# Contributing

Use this repository for public-facing integration examples, connector guidance,
plugin files, and website source. The hosted implementation is maintained
separately; do not copy private source or its Git history into this repository.

Use a focused branch and review the staged files before pushing. Examples may
be synthetic or use reviewed public non-personal data. For public data, record
its license, source URL, attribution, pinned checksum, transformation and timing
assumptions. Public availability alone does not make a dataset suitable. Keep
downloaded data and generated outputs outside Git. Remove secrets, personal contact information, live account/audit
identifiers, and private URLs from screenshots and documentation. Do not submit
security reports containing secrets through public issues; use
[support](https://mlreferee.com/support).

Website contributors should start with [website/README.md](website/README.md).
Plugin contributors should preserve the connection and consent boundaries in
the skill. Update the plugin version when preparing a new public release, but
do not equate a source commit with a directory-approved version.

Before proposing a change:

```sh
python3 scripts/check_public_repo.py
python3 -m unittest discover -s tests -v
claude plugin validate .
claude plugin validate plugins/mlreferee
```

These checks do not establish real OAuth connectivity or directory approval.
No local check should upload data, spend credits, or change account settings.
Never use a force push or replace other contributors' changes as an export step.
