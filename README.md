# ML Referee

Official integrations, agent instructions, and reproducible practice examples for
[mlreferee.com](https://mlreferee.com).

ML Referee evaluates whether candidate features add predictive evidence beyond
a declared baseline for supervised machine learning and forecasting. It also
supports bounded feature repair. Evaluations run on the hosted service; this
repository does not contain its engine or backend implementation.

## Start here

Your first question is simple: **does one proposed input improve prediction
beyond the input you already have?** Start with made-up data so you can learn
the workflow without exposing business data.

1. **Try it locally.** Follow [the first exercise](docs/coding-agents.md#start-locally-no-referee-account-required).
   You need Git and Python 3.10+, but no Referee account. Nothing is uploaded.
2. **Connect your coding agent.** Choose [Codex](docs/codex.md) or
   [GitHub Copilot in VS Code](docs/copilot.md). Use the tested client-specific
   recipe; complete browser consent yourself, then check beta access and credits.
3. **Run the small example.** Follow the [synthetic walkthrough](examples/synthetic-regression/README.md)
   and its [copy-and-paste prompts](examples/synthetic-regression/prompts.md).
   Approve the exact upload first, then approve the returned quote separately.
4. **Keep the evidence.** Save the actual report and receipt privately before
   expiry. Follow [report verification](examples/report-integrity/README.md);
   if only report text is available, use its text-verification instructions.

For an existing account, you can go straight to your client guide. For pending
access, follow the [access and evaluation steps](docs/coding-agents.md#from-connected-to-evaluated).
If something fails, start with [troubleshooting](docs/usage.md#troubleshooting).

### After your first run

- [Bike-demand forecasting](examples/bike-demand/README.md): prepare licensed real
  data, six candidate inputs and a reserved later period.
- [All practice examples](examples/README.md) and [data/consent rules](docs/usage.md).
- [Claude preview integration](docs/claude.md): separate setup and test status.
- [Website source workspace](website/README.md).

## Connect your account with OAuth

ML Referee uses Auth0 to let you authorize supported clients to access your
Referee account. Sign in through the browser and approve the connection; the
client then sends an access token with protected MCP calls. Separate client
registrations serve ChatGPT, hosted Claude, Codex and Copilot in VS Code.
You do not need an Auth0 administrator account or a shared client secret.
Referee still checks beta access, credits and the scope of each operation.
See [how account authorization works](docs/authentication.md), including the
tested status for each client and the separate approval for evaluation spending.

## Integration status

The [coding-agent guides](docs/coding-agents.md) separate runnable local exercises
from hosted connection tests. As of October 19, 2026, the tested scope is:

| Path | Completed | Remaining |
| --- | --- | --- |
| [Codex CLI 0.163.0, macOS](docs/codex.md) | Sign-in; synthetic upload, preflight, approved one-credit evaluation, result/receipt retrieval and report-text fingerprint verification through its managed MCP connection | A complete model-driven conversation, token refresh and new-account onboarding |
| [Copilot 0.65.0 / VS Code 1.137.0, macOS](docs/copilot.md) | Sign-in; model-driven exact-file upload, valid preflight and a one-credit quote using the included [local file adapter](docs/copilot.md#upload-the-configured-file-directly) | Evaluation submission and result retrieval; new-account onboarding |
| [Optional Copilot refresh helper](docs/copilot.md#copilot-refresh-helper-tested-alternative) | Two real refresh exchanges, credential rotation and successful calls after restart | Natural-expiry renewal and long-running sessions; native VS Code refresh is separate and unverified |
| [Hosted Claude web connection](docs/claude.md) | Browser sign-in, authenticated discovery/readiness and refresh-token issuance | Actual refresh exchange, evaluation workflow and directory credential coordination; Claude Code needs its own sign-in test |

The Codex evaluation consumed exactly one beta credit. The Copilot rehearsal
stopped at its quote and consumed none. These are synthetic workflow tests,
not evidence of real-world predictive performance or universal client support.
Private reports, credentials and account identifiers are excluded from this repo.

Start with `python3 scripts/practice.py` for local practice without an account.
Then follow the chosen client guide and the
[staged synthetic example](examples/synthetic-regression/README.md), approving
upload and quoted spending separately. The optional Copilot helper stores
credentials in restricted local JSON files, not the OS keychain; review its
security notes before installing it.

The Claude plugin remains a **preview**. The hosted Claude web connection passed
sign-in and authenticated calls; Claude Code authentication and directory review
remain separate. Installing plugin files alone does not establish a working
connection. See the [Claude status and setup guide](docs/claude.md).

The existing OpenAI submission is under review. This repository does not contain
or replace its submitted ZIP, and it does not imply OpenAI or Anthropic approval.
Discover the tools actually exposed by your connection rather than assuming
that a particular download or evaluation capability exists.

## Repository layout

- `plugins/mlreferee/`: self-contained Claude plugin and workflow skill.
- `.claude-plugin/marketplace.json`: publisher-managed Claude Code catalog.
- `docs/`: public connection and usage guidance.
- `examples/`: synthetic inputs, public-data preparation, agent prompts, and local hashing.
- `website/`: reserved for website source and public assets.

Private engine code, production deployment tooling, customer reports, reviewer
accounts, credentials, and operator records do not belong here. Website changes
should stay separate from the installable plugin. See [contributing](CONTRIBUTING.md).

## License and help

Public integration code, workflow instructions, and synthetic examples are
[MIT licensed](LICENSE). ML Referee branding and the hosted service are excluded;
see [NOTICE](NOTICE). This is not an open-source release of the evaluation engine.
Downloaded third-party datasets retain their own licenses; see each example's
source notice. Data preparation runs locally without a Referee account. Hosted
evaluations require a working connection, approval, credits, and your permission.

[Website](https://mlreferee.com) · [Support](https://mlreferee.com/support) ·
[Beta access](https://mlreferee.com/beta) · [Privacy](https://mlreferee.com/privacy) ·
[Terms](https://mlreferee.com/terms)
