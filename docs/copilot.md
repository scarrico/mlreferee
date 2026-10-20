# Practice with GitHub Copilot in VS Code

This is a coding-workspace walkthrough, not Microsoft Copilot, a browser
chatbot, GitHub's cloud coding agent, or the separate Copilot CLI. Those surfaces
must not inherit a VS Code compatibility claim.

**Status:** local exercises are runnable. Referee authentication from a fresh
Copilot/VS Code installation has not been verified. The connection section is
a rehearsal guide, not a claim of a working integration or free-tier support.

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

## 2. Connect only when a supported sign-in recipe is available

Ask [ML Referee support](https://mlreferee.com/support) for the tested MCP endpoint
and the approved **public** OAuth client ID for your VS Code setup. The publisher
must arrange the redirect and permission settings; users must not create Auth0
applications or obtain shared secrets. Do not assume a Claude or ChatGPT client
configuration works here.

Microsoft documents **MCP: Add Server** in the Command Palette for adding an HTTP
server. Configuration differs by agent harness and destination. Use the exact
publisher-tested destination and settings; review trust and browser sign-in
prompts. Do not overwrite an existing MCP configuration.

For a VS Code-format configuration, Microsoft documents `servers`, `type: http`,
`url`, and `oauth.clientId`. This non-active template illustrates that format:

```json
{
  "servers": {
    "mlreferee": {
      "type": "http",
      "url": "CONFIRMED_MCP_URL",
      "oauth": { "clientId": "PUBLISHER_PUBLIC_CLIENT_ID" }
    }
  }
}
```

Do not install these placeholders. A Copilot-specific configuration file may
use a different schema; do not copy this into it unchanged. No active workspace
MCP configuration is shipped in this repository. Complete sign-in in the browser,
not in the agent prompt. Never place tokens or passwords in configuration examples.

## 3. Verify an actual tool call

Ask the agent:

> Use ML Referee's live MCP tools to discover its schema and check my readiness
> and credits. Show which tool returned the answer. Do not request beta access,
> upload files or submit an evaluation. If tools are missing or sign-in fails,
> stop and explain what is unverified. Do not substitute an invented result.

Inspect the expanded tool output. Tool discovery alone does not prove account
access; successful sign-in does not grant beta approval or credits. Follow the
[shared staged workflow](coding-agents.md) only after readiness succeeds.

## Acceptance before calling this supported

Record the VS Code version, Copilot extension/harness, OS and test date. Test
fresh sign-in without prior Referee tokens, an authenticated readiness call,
beta status and credits, and a later call after a real token refresh. A hosted
example additionally requires approved upload and quote, completed result,
and private artifact preservation. Keep all these items pending until observed.

## Official references

- [Adding and checking MCP servers](https://code.visualstudio.com/docs/agent-customization/mcp-servers)
- [MCP configuration formats](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)

These document client capabilities, not a verified ML Referee connection.
