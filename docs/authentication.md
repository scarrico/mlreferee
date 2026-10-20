# Connect your client to your Referee account

ML Referee uses Auth0 for OAuth authorization. You sign in to Referee in your
browser and grant a supported client permission to act on your behalf. This is
the familiar account-connection pattern used by services that let another
application access your account.

Auth0 is Referee's identity and authorization provider. MCP carries the tool
calls; OAuth authorizes protected calls. You do not need an Auth0 administrator
account, an Auth0 application of your own, or a shared application secret.

## What happens when you connect

1. Your client starts the Referee connection using its published setup guide.
2. You sign in on the Referee browser page and review the requested permissions.
3. Auth0 issues an access token for the Referee API to that client. The client
   supplies it with subsequent protected requests; you do not paste tokens into
   a conversation.
4. Referee validates the token's issuer, audience, expiration and scopes, maps
   the authenticated identity to its private account, and checks service access
   and credits before performing the requested operation.

Referee has separate OAuth client registrations for ChatGPT, hosted Claude,
Codex and Copilot in VS Code. The configured Referee API permissions are
`audit:read` and `audit:write`. Where offline access is authorized and supported,
refresh tokens let the client renew access; issuance alone does not establish
that a client's renewal behavior works.

An OAuth grant permits access to Referee. It does not grant access to your email
mailbox, transfer your other applications' chat histories, approve beta access,
allocate credits, or authorize spending them. Use the same Referee account and
sign-in method across clients when you intend to use the same service account;
matching email strings alone do not establish the same identity.

## Which clients have been checked?

Recorded October 20, 2026. These checks describe the tested client and surface.

| Client | Verified connection | Remaining checks |
| --- | --- | --- |
| ChatGPT | Authenticated calls; an approved synthetic evaluation completed | Public plugin approval remains separate |
| [Codex CLI 0.163.0 on macOS](codex.md) | Browser sign-in and protected calls through managed MCP; synthetic evaluation and report-text verification | Completed model-driven conversation, refresh and new-account onboarding |
| [GitHub Copilot 0.65.0 in VS Code 1.137.0 on macOS](copilot.md) | Browser sign-in and protected calls; model-driven exact-file synthetic upload, preflight, approved one-credit evaluation, report/receipt retrieval and local report-text SHA verification | Native refresh, new-account onboarding and other evaluation paths |
| [Hosted Claude web connection](claude.md) | Browser sign-in, authenticated discovery/readiness and refresh-token issuance | Actual refresh exchange, evaluation workflow and directory credential coordination |
| Claude Code | Public plugin files and instructions available | Its own authenticated connection rehearsal |

The optional Copilot helper passed two refresh exchanges with token rotation
and protected calls after restart. Natural-expiry and long-running behavior
remain unverified. Its local credential storage differs from native clients;
review the [helper's security notes](copilot.md#copilot-refresh-helper-tested-alternative).

## Start with your client guide

Choose [Codex](codex.md), [Copilot in VS Code](copilot.md), or
[Claude](claude.md). Follow the exact endpoint and configuration for that client;
the generic service endpoint alone does not configure every OAuth client.

Keep upload permission and evaluation spending explicit. Check readiness and
credits, approve the intended file upload, then review and authorize the actual
quote. Connecting an account does not authorize arbitrary evaluations.

For connection problems or account/privacy requests, use
[Referee support](https://mlreferee.com/support). Include your client/version and
a sanitized error. Never send passwords, client secrets, access tokens, complete
authorization URLs or datasets. See [Privacy](https://mlreferee.com/privacy) for
how Referee and its providers handle connection data.
