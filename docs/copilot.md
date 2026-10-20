# Practice with GitHub Copilot in VS Code

This is a coding-workspace walkthrough, not Microsoft Copilot, a browser
chatbot, GitHub's cloud coding agent, or the separate Copilot CLI. Those surfaces
must not inherit a VS Code compatibility claim.

**Verified October 19–20, 2026:** first sign-in and authenticated MCP calls passed
on macOS with VS Code 1.137.0 and the official GitHub Copilot integration 0.65.0.
The optional pinned helper below also passed two real refresh-token exchanges,
rotation, and a post-restart Copilot check. Native VS Code refresh remains
unverified. A model-driven synthetic rehearsal with the local file adapter
passed exact-byte upload, free preflight and a one-credit quote after an initial
inline CSV attempt was rejected (see below). On October 20, one explicitly
approved synthetic evaluation completed through the model-driven Copilot session;
the report and receipt were retrieved, and a locally computed report-text SHA-256
returned `digest_match`. Exactly one beta credit was consumed. This establishes
the bounded workflow on this setup, not compatibility with every Copilot surface
or subscription; natural-expiry and multi-day endurance remain untested.

## 1. Open the public repository

Clone this repository and open its folder in VS Code. Use a local Copilot agent
session with terminal/file tools available. Review workspace trust before
enabling tools; do not enable blanket automatic tool approval.

Follow [the shared first exercise](coding-agents.md). Explicitly ask Copilot to
read AGENTS.md; do not rely on automatic instruction discovery. Approve only
the local commands described there. Python 3.10+ is the only exercise runtime.

Expected: a 400-row synthetic fixture passes structural checks, preparation
tests pass, and the fingerprint exercise detects changed bytes. Nothing is
uploaded and no Referee credits are used. Copilot's own usage limits are separate.

Then use [the bike-demand walkthrough](../examples/bike-demand/README.md) and its
[staged prompts](../examples/bike-demand/prompts.md) to prepare real public data.
You can do every local preparation step before connecting Referee.

## 2. Connect Referee in VS Code

Sign in to GitHub Copilot in VS Code using your own account. Referee sign-in is
separate: you will authorize it in a browser when you first call a protected tool.
You do not need an Auth0 administrator account or a client secret. The publisher
has registered a dedicated public OAuth client for this connection.

Create `.vscode/mcp.json` in your local workspace, or merge the `mlreferee` entry
into its existing `servers` object. Preserve other servers and settings. This is
the VS Code desktop format, not a configuration for the separate Copilot CLI.

For a native connection without the helper, use this first-login-tested
configuration. For tested refresh exchanges, use the alternative
[helper setup below](#copilot-refresh-helper-tested-alternative); do not configure
both simultaneously under the same name.

```json
{
  "servers": {
    "mlreferee": {
      "type": "http",
      "url": "https://api.mlreferee.com",
      "oauth": { "clientId": "tpc_2rLZHkjkETGk23PQE9inri" }
    }
  }
}
```

The client ID is public, not a secret. No active workspace MCP configuration is
shipped in this repository: adding it is your explicit connection step. Use
**MCP: List Servers** to find and start `mlreferee`, and review VS Code's trust
prompts. Enable its tools in your local Copilot agent session; keep approvals on.

## 3. Verify an actual tool call

Ask the agent:

> Use ML Referee's live MCP tools: describe_referee, get_referee_readiness, and
> get_credits. Show which tool returned each answer. Do not request beta access,
> upload files or submit an evaluation. If tools are missing or sign-in fails,
> stop and explain what is unverified. Do not substitute an invented result.

`describe_referee` and `get_referee_readiness` can work before sign-in; readiness
may correctly report missing credentials. The protected, read-only `get_credits`
call triggers browser sign-in and consent. Review the Referee authorization screen
yourself and return to VS Code when finished. Never paste passwords, tokens, or
authorization URLs into the agent conversation.

Inspect the expanded tool output. The rehearsal discovered 26 tools and confirmed
connected, authorized, ready responses after sign-in. Tool counts may change;
discover current schemas rather than treating this count as a contract. Successful
sign-in does not grant beta approval or credits. If your account is pending, stop
and follow the beta-access instructions before attempting an evaluation.

Follow the [shared staged workflow](coding-agents.md) only after access is ready:
approve data upload, inspect preflight and the quote, then separately authorize
the evaluation. Connecting alone does not authorize any of those actions.

## What remains unverified

- **Native persistent sign-in:** the native authorization request did not request
  `offline_access`. A successful first login does not establish refresh behavior.
  The tested VS Code schema does not offer an `oauth.scopes` setting; do not add
  unsupported fields or assume automatic renewal works.
- **Long-running helper sessions:** real early refresh exchanges and restart
  passed, but natural expiry, idle/maximum-lifetime expiry, token revocation and
  multi-process contention were not exercised. Reauthorization may still be needed.
- **New-user onboarding:** this rehearsal used an existing Referee account, not
  a newly approved beta account or a new credit grant.
- **Other evaluation paths:** the single-candidate synthetic regression workflow
  passed. Campaigns, repair, provided-score mode and the bike-demand example have
  not received a complete Copilot evaluation rehearsal.
- **Other environments:** Windows, Linux, remote workspaces, browser VS Code,
  and other Copilot surfaces need separate verification.

## Synthetic upload rehearsal: stopped before transmission

On October 19, 2026, the helper-backed Copilot agent completed live schema and
readiness checks and read the unchanged public synthetic fixture and contract.
The owner authorized upload, free preflight and a quote only, not submission.
The proposed raw-CSV MCP upload requested 86,400-second retention and contained
400 data rows, but its bytes did not match the approved local file:

| Artifact | Bytes | SHA-256 |
| --- | --- | --- |
| Public `examples/synthetic-regression/example.csv` | 46,785 | `98d7ffbc1707e0044832e54cc859e1010326799f6d409d18ac4e350e21892c45` |
| Proposed tool argument, rejected before upload | 46,749 | `c9089b98d937b8151486af614aa590e26d8849bd68babdfbd9b3376343480087` |

The one-time upload confirmation was declined. No dataset was uploaded, no
preflight or quote was obtained, and no evaluation was submitted in this test.
This is an input-delivery failure, not a Referee statistical result or a claim
that authentication failed. Copilot/provider usage is separate from Referee
evaluation credits.

Do not treat a model's reconstruction of CSV text as an exact file transfer,
even if row and column counts agree. Before approving a raw-data upload, compare
the exact decoded tool argument's UTF-8 bytes with the original file. If they
differ, stop; do not silently change the fixture or approve a near-match. A
file adapter below addresses this by reading the configured file itself.

The subsequent model-driven rehearsal through this same Copilot connection
passed with the adapter:

- One upload returned a server input manifest with **46,785 bytes** and SHA-256
  **`98d7ffbc1707e0044832e54cc859e1010326799f6d409d18ac4e350e21892c45`**, exactly
  matching the original file. Retention was **86,400 seconds**.
- Actual preflight returned **`valid: true`**, **400 rows**, **6 columns**, and
  **`baseline_mode: generic_refit`**.
- The preflight and quote arguments preserved every field of the unchanged
  public contract: regression, one baseline, the full one-candidate family,
  five expanding folds, and `scope: feature_quality_only` under `general_ml`.
- The actual quote cost was **1 beta credit**. A stable quote idempotency key
  was used. The agent stopped at the quote: no evaluation was submitted and no
  Referee credit was consumed or reserved by this rehearsal.

The first adapter response put local verification evidence in an additional
text block; Copilot preferred the structured service result and omitted that
block. The server manifest itself was independently inspected and matched. The
adapter now also places the local evidence in `structuredContent`, with an
offline regression assertion for that client behavior. This presentation fix
was not used to justify another upload. Account, upload and quote identifiers
are intentionally omitted here.

## Completed evaluation and report verification — October 20, 2026

With explicit approval for at most one beta credit, the same Copilot session
completed the remaining steps using the existing, unexpired exact-file upload:

1. Rechecked live readiness, credits and preflight; preflight remained valid for
   400 rows, six columns and `generic_refit`.
2. Obtained a fresh one-credit quote because the prior day's quote had expired.
   Every public contract field was preserved. A stable quote key and a separate
   stable submission key were used.
3. Submitted once, checked the audit's completion, and retrieved the actual result
   and receipt. No second evaluation was created.
4. Read the exact `result.report` string from Copilot's saved MCP tool-result
   JSON artifact and wrote its UTF-8 bytes directly into a private report file,
   without a model reconstruction, line-ending conversion or added newline.
5. Ran the public `hash_report.py --text-file` utility on that actual file. The
   saved text was 2,332 bytes; its independently computed SHA-256 was sent to
   `verify_audit_report` with `representation: report_text`. The service returned
   **`digest_match`** for the same audit.
6. Compared actual before/after credit responses: exactly **one beta credit
   consumed**, one fewer available, and **zero reserved** after completion.

The report and receipt were saved in an owner-only private directory outside
this repository; no audit or input was deleted. Save artifacts before the input
retention expires—evaluation completion does not reset the retention clock.
Raw responses, account/audit/quote IDs, absolute balances and reports are excluded
from public evidence. The result remains a synthetic feature-quality opinion;
fingerprint consistency does not establish correctness or real-world value.

This check verified report **text**, not an original downloaded result-JSON file.
The existing connector did not gain a hosted download feature. To reproduce the
save step, use the client's exact tool-result artifact when available, parse its
returned report string, and write UTF-8 bytes directly; do not copy a rendered
chat bubble. Client-specific artifact paths are private and vary by session.

### Upload the configured file directly

The public `scripts/file_upload_mcp.mjs` adapter adds one **local** tool,
`upload_private_dataset_file`, in front of the existing authenticated stdio
transport. Its small arguments contain the expected file SHA-256 and retention;
the model never reconstructs the CSV. The adapter reads the one configured file,
preserves its exact UTF-8 bytes, and calls the existing service upload tool. It
checks the returned input manifest's SHA-256 and byte count before reporting a
match. It does not add a hosted tool or change the published connector package.

Use the helper setup below first. Stop only `mlreferee` in **MCP: List Servers**.
In that server's `args` array, insert these arguments **before** the existing
`mcp-remote/dist/proxy.js` path, retaining all later arguments and the existing
credential-directory environment setting:

```json
"${workspaceFolder}/scripts/file_upload_mcp.mjs",
"--file", "${workspaceFolder}/examples/synthetic-regression/example.csv",
"--format", "csv",
"--", "node"
```

This recipe assumes VS Code opened this public repository. If your workspace is
elsewhere, use absolute paths to the adapter and the exact approved input file.
Use your Node executable's absolute path instead of the inner `node` argument if
VS Code cannot find it. Preserve the outer server `command` and OAuth options.
Restart the server, review its configuration/trust prompt, and keep tool
approvals enabled. Only the configured file is available to the added tool;
the agent cannot choose another path through its arguments. Changing the file
configuration requires reviewing and authorizing the newly selected dataset.

Check the original file locally:

```sh
shasum -a 256 examples/synthetic-regression/example.csv
node --test tests/file_upload_mcp.test.mjs
```

After explicitly authorizing that synthetic upload, ask Copilot:

> Use upload_private_dataset_file with the locally computed expected_sha256
> and retention_seconds 86400. Do not reconstruct or paste CSV into another
> tool. Confirm local_file_verification.server_manifest_match is true, then
> preflight this upload using the unchanged synthetic contract.json and obtain
> one quote with a stable quote idempotency key. Show cost, scope and retention.
> Stop before submission or credit spending. On a hash mismatch or uncertain
> upload outcome, stop without retrying or reconnecting.

The adapter accepts regular, non-symlink CSV/JSON files up to 1,000,000 bytes and
rejects invalid UTF-8. All beta-data and consent requirements still apply; a
checksum does not certify a dataset's suitability. Keep private files outside
this public repository. The adapter uses Node's standard library and leaves
credential handling with the configured transport. It does not read token files
or log datasets. Existing transport logging/privacy considerations still apply.
This is a file-transfer helper, not a sandbox or an authorization system:
the original remote tools remain available, and the client must still obtain
your approval for uploads and evaluation spending.

Within one adapter session, repeating the same completed file/retention request
returns the saved upload result without another upload. This is not server-side
idempotency or persistence across restarts. After any failed/uncertain upload,
recover its returned identifier if available or contact support; do not restart
the adapter to bypass the one-attempt guard. Removing the adapter arguments and
restarting restores the original helper configuration.

## Copilot refresh helper: tested alternative

The native connection above did not request `offline_access`. A separate,
Copilot-only rehearsal tested the pinned third-party OAuth helper
`mcp-remote@0.15.1` on macOS with Node.js 25.8.1. Results on October 19, 2026:

- Fresh browser consent included offline access; a refresh token was issued.
- Two sequential real `refresh_token` exchanges returned HTTP 200. Each returned
  a different refresh token; the second used the saved rotated token.
- A protected read-only `get_credits` call succeeded after each exchange.
- After restarting the helper, Copilot's actual `get_credits` and
  `get_referee_readiness` outputs confirmed connected/authorized/ready status
  with the balance unchanged. No new browser consent was needed.
- The credential directory was mode `0700`; token JSON files were mode `0600`.

The bounded test invoked the pinned helper's own refresh method early, while
the VS Code instance was stopped to avoid concurrent refreshes. It did not
edit cached expiry times, shorten shared token lifetimes, or replay an old token.
This proves refresh issuance, exchange, rotation and reuse after restart—not
natural-expiry scheduling or multi-day endurance. No evaluation was submitted.

The rehearsal uses a dedicated public client, authorization code with PKCE,
`audit:read audit:write offline_access`, no client secret, and the existing
loopback callback `http://127.0.0.1:33418/`. It does not change the backend,
ChatGPT, Claude, Codex, or their registrations.

One compatibility issue was reproduced: the helper normalized the API resource
identifier to `https://api.mlreferee.com/`, while Auth0's configured audience is
exactly `https://api.mlreferee.com`. The isolated test configuration now uses
the helper's supported `--disable-resource-parameter` and
`--authorize-param audience=https://api.mlreferee.com` options, alongside
`--host 127.0.0.1`, `--callback-path /`, port `33418`, and `--transport http-only`.
This uses Auth0's audience parameter; it is not a general MCP resource-indicator
recommendation.

### Local desktop setup

This helper is optional third-party software: review the security notes below
before installing it. Install Node.js/npm first. The tested runtime was Node.js
25.8.1; other runtime versions need their own check. No administrator privileges
or Auth0 configuration are needed. The commands below use stable user-local
paths rather than the temporary directories used for the rehearsal:

```sh
umask 077
mkdir -p "$HOME/.local/share/mlreferee-copilot/helper" "$HOME/.local/share/mlreferee-copilot/auth"
chmod 700 "$HOME/.local/share/mlreferee-copilot" "$HOME/.local/share/mlreferee-copilot/auth"
npm install --prefix "$HOME/.local/share/mlreferee-copilot/helper" --ignore-scripts --save-exact mcp-remote@0.15.1
```

Keep the generated package lock for repeatable dependency installation. Installing
again later may otherwise resolve different transitive versions. Stop the native
`mlreferee` entry with **MCP: List Servers → Stop Server**, then replace only that
entry in `.vscode/mcp.json` with:

```json
{
  "servers": {
    "mlreferee": {
      "type": "stdio",
      "command": "node",
      "args": [
        "${userHome}/.local/share/mlreferee-copilot/helper/node_modules/mcp-remote/dist/proxy.js",
        "https://api.mlreferee.com",
        "33418",
        "--host", "127.0.0.1",
        "--callback-path", "/",
        "--transport", "http-only",
        "--disable-resource-parameter",
        "--authorize-param", "audience=https://api.mlreferee.com",
        "--static-oauth-client-info", "{\"client_id\":\"tpc_2rLZHkjkETGk23PQE9inri\",\"token_endpoint_auth_method\":\"none\"}",
        "--static-oauth-client-metadata", "{\"scope\":\"audit:read audit:write offline_access\",\"grant_types\":[\"authorization_code\",\"refresh_token\"],\"token_endpoint_auth_method\":\"none\"}"
      ],
      "env": {
        "MCP_REMOTE_CONFIG_DIR": "${userHome}/.local/share/mlreferee-copilot/auth"
      }
    }
  }
}
```

Preserve other server entries. If VS Code cannot find `node`, set `command` to
your installed Node executable's absolute path. This example uses VS Code's
documented `${userHome}` substitution; the live rehearsal used absolute paths.
Keep these folders out of repository, shared-folder and cloud-sync locations.

Start the server, approve its trust prompt, and run the read-only verification
prompt in section 3. Review the browser screen for **ML Referee Copilot**, audit
read/write, **Allow offline access**, and the exact local callback above. Sign in
with your Referee account—not your email mailbox or Auth0 administrator account.
Then stop/start the server and repeat the protected read-only call. Do not
manually copy or rotate tokens. If port 33418 is occupied, stop the conflicting
test instance; do not invent an unregistered callback or widen OAuth settings.

Security notes for this optional helper:

- It is third-party software, not an official VS Code credential component.
  The rehearsal pinned version 0.15.1, disabled installation scripts, and npm's
  audit reported no known vulnerabilities at installation time. That is not a
  security guarantee.
- It stores OAuth credentials as local JSON, not in the OS keychain. Use an
  owner-only dedicated directory outside repositories and shared/synced folders
  via `MCP_REMOTE_CONFIG_DIR`. Do not expose, commit, or send its contents.
- Keep debug logging off. Even normal authorization logs can contain private
  authorization URLs; do not publish raw output or transcripts.
- Do not clear a shared `~/.mcp-auth` folder or revoke unrelated connections
  while troubleshooting. Keep tool approvals enabled.

To return to the native connection, stop only this helper and restore the native
entry in section 2. Do not delete shared credential stores. Disconnect/revoke only
this Copilot authorization if you no longer want its offline access; merely
stopping the process does not revoke already issued credentials.

## Troubleshooting

The tested desktop callback is `http://127.0.0.1:33418/`, including its trailing
slash. A callback mismatch interrupted the first attempt and was corrected in
the publisher's client registration. Users should not edit OAuth provider
settings or share a secret to work around a sign-in error.

If sign-in fails or later expires, stop hosted actions and contact
[support](https://mlreferee.com/support) with your client version and a sanitized
error. Never send tokens, full authorization URLs, datasets or raw transcripts.

## Official references

- [Adding and checking MCP servers](https://code.visualstudio.com/docs/agent-customization/mcp-servers)
- [MCP configuration formats](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)
- [mcp-remote source and configuration](https://github.com/punkpeye/mcp-remote)

These document client capabilities. The narrower test results above describe
what was actually verified with ML Referee.
