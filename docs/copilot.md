# Practice with GitHub Copilot in VS Code

This is a coding-workspace walkthrough, not Microsoft Copilot, a browser
chatbot, GitHub's cloud coding agent, or the separate Copilot CLI. Those surfaces
must not inherit a VS Code compatibility claim.

**Verified October 19, 2026:** first sign-in and authenticated MCP calls passed
on macOS with VS Code 1.137.0 and the official GitHub Copilot integration 0.65.0.
The optional pinned helper below also passed two real refresh-token exchanges,
rotation, and a post-restart Copilot check. Native VS Code refresh remains
unverified. No evaluation was run or ML Referee credits spent. This is not a full
evaluation acceptance test or a claim of compatibility with every Copilot surface
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
- **Full evaluation:** uploads, preflight, quotes, evaluation submission and
  result retrieval were not exercised in this connection test.
- **Other environments:** Windows, Linux, remote workspaces, browser VS Code,
  and other Copilot surfaces need separate verification.

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
