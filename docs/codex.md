# Use ML Referee examples with Codex

You can use Codex to prepare the files, explain their columns, and guide an
authorized evaluation. You do not need to write an API client to try the local
examples. A local folder alone does not give Codex access to ML Referee.

Prefer another coding agent? See [the shared workflow and Copilot guide](coding-agents.md).

## 1. Open the repository

```sh
git clone https://github.com/scarrico/mlreferee.git
cd mlreferee
```

In the Codex desktop app, open this folder and start a task in it. In the CLI,
run `codex` from this directory. Codex should read `AGENTS.md` before working.
Do not open the private service repository or give the agent unrelated data.

Paste this first:

> Read AGENTS.md and docs/coding-agents.md, then run python3 scripts/practice.py.
> Explain the local checks and the remaining service prerequisites. Do not
> change connection settings, upload data or spend credits.

Then, for real public data:

> Read AGENTS.md, examples/README.md, and examples/bike-demand/README.md.
> Walk me through the bike-demand example. You may download the pinned public
> UCI archive and run the local preparation and checks. Do not upload data to
> ML Referee, request beta access, redeem invitations, submit evaluations,
> change connection settings, or spend credits. Show me the exact files,
> candidate list, timing assumptions, and remaining prerequisites. Stop there.

For a smaller first exercise, substitute `examples/synthetic-regression/README.md`
and ask it to use the included fixture without any download.

## 2. Connect Codex CLI

**Tested October 19, 2026:** local macOS, official Codex CLI **0.163.0**. Fresh
Codex OAuth login and real discovery/readiness tool calls succeeded through
Codex's own app-server using its managed credentials. The browser used an
existing Referee account session and new consent; new-account signup was not
tested. Refresh and a complete evaluation remain separate acceptance checks.
See [the detailed test status](codex-auth-readiness.md).

Codex desktop, the IDE extension, Windows, Linux, remote environments and Copilot
have not inherited this pass. CLI 0.144.4 failed this sign-in rehearsal; do not
use it for these instructions.

### Use the tested version

The rehearsal used the official package through npm without replacing the
globally installed CLI. With Node.js/npm installed, check the pinned version:

```sh
npm exec --yes --package=@openai/codex@0.163.0 -- codex --version
```

This downloads/runs a coding client, not a website or Referee server dependency.
The local Python examples still need no Node.js. Use the pinned command below
throughout so an older `codex` on PATH is not used accidentally.

### Add the public connection settings

Review your personal Codex `config.toml` (normally `~/.codex/config.toml`). Merge
only the entry below; preserve all unrelated settings. If `mlreferee` is already
defined, inspect it first rather than adding duplicate tables or replacing a
working connection. These are public client settings, not account credentials:

```toml
[mcp_servers.mlreferee]
url = "https://api.mlreferee.com"
scopes = ["audit:read", "audit:write", "offline_access"]

[mcp_servers.mlreferee.oauth]
client_id = "tpc_wwg2x8UbJtLAcCPHS6c6dP"
callback_port = 63219
callback_url = "http://127.0.0.1:63219/callback/YknuSF0-CSr-"
```

Keep the URL and callback exactly as shown. The publisher registered this fixed
loopback callback; do not append `/mcp`, add a trailing slash, choose another
port, or add an `oauth_resource` override. Port 63219 must be free on the local
machine. A callback that works on your laptop does not automatically work from
a remote machine. Customers do not need an Auth0 dashboard or client secret.

### Sign in and check access

```sh
npm exec --yes --package=@openai/codex@0.163.0 -- codex mcp login mlreferee --scopes audit:read,audit:write,offline_access
npm exec --yes --package=@openai/codex@0.163.0 -- codex mcp list
npm exec --yes --package=@openai/codex@0.163.0 -- codex
```

In the browser, use your ML Referee sign-in method and review the
**ML Referee Codex** consent screen. The scopes allow reading results, submitting
authorized work, and maintaining sign-in. Consent is not approval to upload
every local file or spend credits without your instructions. Never paste
passwords, tokens, authorization URLs or secrets into an agent prompt.

In the CLI, `/mcp` lists connections. Then ask:

> Use ML Referee's live describe_referee and get_referee_readiness tools.
> Report connection, access and credit status from their actual responses.
> Do not request beta access, upload data, quote or submit an evaluation.
> If tools are absent or authentication fails, stop and explain the error.

Inspect the tool calls, not just the prose answer. A listed server is not proof
of a working connection. Sign-in does not automatically approve beta access or
allocate credits. If access is pending, request beta access only with your
permission, wait for human approval, and recheck readiness before proceeding.

### Troubleshooting

The first two errors below were observed in the rehearsal. The remaining rows
are general guidance, not additional observed failures.

| Symptom | What to check |
| --- | --- |
| `resource parameter must be a string` | Remove an explicit `oauth_resource` override from this connection; it duplicated the resource parameter in the tested clients |
| Auth0 `Service not found` with a trailing-slash resource | CLI 0.144.4 generated the wrong resource; the tested 0.163.0 discovery path worked without an override |
| Callback rejected or local port unavailable | Compare the exact callback and listener port above; do not loosen provider redirect rules |
| Connected but no usable credits | Check beta approval and readiness; do not retry submissions |

For other errors, use [support](https://mlreferee.com/support) with the client
version and a sanitized message. The [official MCP guide](https://developers.openai.com/codex/mcp)
explains Codex's general connection controls; the specific test scope is recorded here.

## 3. Run the example in deliberate stages

Use the [bike-demand prompts](../examples/bike-demand/prompts.md) or
[synthetic prompts](../examples/synthetic-regression/prompts.md) one at a time.
They separate permission to upload from permission to spend credits. Do not
paste all stages together as one instruction.

Before submission, you should see:

- The outcome and prediction time, baseline, full candidate family, and validation plan.
- The exact CSV and contract being uploaded; the reserved holdout is excluded.
- The live preflight response and a quote with its scope and actual credit cost.
- A request for your explicit approval of that quote.

After submission, ask Codex to save what the live tools actually return in your
local `outputs/` folder, explain the result in plain language, and propose next
research steps. Saving a rendered MCP response is not the same as downloading
the original report bytes. Use the [integrity guide](../examples/report-integrity/README.md)
only with the correct original artifact.

## 4. A useful final answer from your agent

Ask for this compact structure, filled from the real report:

> **Question and comparison:** what was evaluated against what?
> **Evidence:** which candidates were supported, provisional, unresolved, or
> showed no incremental evidence, using the service's actual findings?
> **Next work:** which uncertainty suggests collecting more relevant observations,
> improving a measurement, or testing a revised hypothesis?
> **Limits:** what does this result not establish about future data?
> **Artifacts:** where are the saved report, receipt, and declared contract?

An unresolved feature is not automatically useless. A supported feature is not
automatically ready for production. Keep follow-up experiments separate and
seek approval before using the holdout or spending more credits.
