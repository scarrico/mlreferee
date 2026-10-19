# ML Referee

Official integrations, agent instructions, and synthetic examples for
[mlreferee.com](https://mlreferee.com).

ML Referee evaluates whether candidate features add predictive evidence beyond
a declared baseline for supervised machine learning and forecasting. It also
supports bounded feature repair. Evaluations run on the hosted service; this
repository does not contain its engine or backend implementation.

## Start here

- [Claude connector and plugin](docs/claude.md)
- [Synthetic regression example and agent prompts](examples/synthetic-regression/README.md)
- [Compute report SHA-256 locally](examples/report-integrity/README.md)
- [Accounts, data, consent, and limitations](docs/usage.md)
- [Website source workspace](website/README.md)

## Integration status

The Claude plugin is a **preview**, not a directory-approved or authenticated
Claude release. Its connection configuration is prepared for the Claude endpoint;
server activation, OAuth configuration, and a real Claude sign-in rehearsal are
still required. Installing files alone does not establish a working connection.

The existing OpenAI submission is under review. This repository does not contain
or replace its submitted ZIP, and it does not imply OpenAI or Anthropic approval.
The new agent download tool is not deployed; discover the tools actually exposed
by your connection rather than assuming it exists.

## Repository layout

- `plugins/mlreferee/`: self-contained Claude plugin and workflow skill.
- `.claude-plugin/marketplace.json`: publisher-managed Claude Code catalog.
- `docs/`: public connection and usage guidance.
- `examples/`: synthetic input data, prompts, and a local-only hashing utility.
- `website/`: reserved for website source and public assets.

Private engine code, production deployment tooling, customer reports, reviewer
accounts, credentials, and operator records do not belong here. Website changes
should stay separate from the installable plugin. See [contributing](CONTRIBUTING.md).

## License and help

Public integration code, workflow instructions, and synthetic examples are
[MIT licensed](LICENSE). ML Referee branding and the hosted service are excluded;
see [NOTICE](NOTICE). This is not an open-source release of the evaluation engine.

[Website](https://mlreferee.com) · [Support](https://mlreferee.com/support) ·
[Beta access](https://mlreferee.com/beta) · [Privacy](https://mlreferee.com/privacy) ·
[Terms](https://mlreferee.com/terms)
