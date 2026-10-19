# Public ML Referee integration repository

This repository contains public integrations, instructions, reviewed examples,
and website source. It is not the service implementation repository.

- Use `mlreferee` for repository names, plugin IDs, folders, MCP keys and commands.
- Keep installable Claude components inside `plugins/mlreferee/`. Website work
  belongs in `website/`; do not put website dependencies or builds in the plugin.
- Never add private engine code/history, operator records, customer data/reports,
  real account identifiers, reviewer credentials, client secrets, tokens, signed
  transfer links, logs, databases, or production deployment configuration.
- Examples may use synthetic data or reviewed, licensed public non-personal
  datasets. Public availability alone is not permission or a privacy review.
  Record source, license, attribution, checksum, transformations, and timing
  assumptions. Download third-party data locally; do not commit datasets or
  generated reports. Do not imply anonymization or a passing preflight
  automatically establishes legal compliance.
- Preserve authorization before uploading data or spending credits, and all
  financial-advice, model-safety, and deployment-certification boundaries.
- Do not claim that a preview integration or a pending tool is live or approved.
  Discover current tool schemas. Do not expose the pending agent download tool
  or replace the OpenAI submission as part of public documentation work.
- Our public integration/preparation code and synthetic examples are MIT;
  third-party datasets retain their own licenses. Branding and the hosted engine
  are excluded. Preserve LICENSE and NOTICE, including third-party notices.
- Do not commit recordings or large binaries. Link to separately hosted videos.
- Run `python3 scripts/check_public_repo.py`, `claude plugin validate .`, and
  `claude plugin validate plugins/mlreferee` after relevant edits.
- Do not enable a site deployment, edit OAuth, or deploy the server unless the
  owner explicitly requests that separate action.
