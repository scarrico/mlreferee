# Practice with GitHub Copilot in VS Code

This is a coding-workspace walkthrough, not Microsoft Copilot, a browser
chatbot, GitHub's cloud coding agent, or the separate Copilot CLI. Those surfaces
must not inherit a VS Code compatibility claim.

**Verified October 19, 2026:** first sign-in and authenticated MCP calls passed
on macOS with VS Code 1.137.0 and the official GitHub Copilot integration 0.65.0.
No evaluation was run or ML Referee credits spent. Persistent sign-in and token
refresh remain unverified; this is not a full evaluation acceptance test or a
claim of compatibility with every Copilot surface or subscription.

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

Use the tested configuration:

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

- **Persistent sign-in:** the observed authorization request did not request
  `offline_access`. A successful first login does not establish refresh behavior.
  The tested VS Code schema does not offer an `oauth.scopes` setting; do not add
  unsupported fields or assume automatic renewal works.
- **New-user onboarding:** this rehearsal used an existing Referee account, not
  a newly approved beta account or a new credit grant.
- **Full evaluation:** uploads, preflight, quotes, evaluation submission and
  result retrieval were not exercised in this connection test.
- **Other environments:** Windows, Linux, remote workspaces, browser VS Code,
  and other Copilot surfaces need separate verification.

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

These document client capabilities. The narrower test results above describe
what was actually verified with ML Referee.
