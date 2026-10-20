# Codex sign-in: implementation and verification process

Status: **planned; ML Referee end-to-end Codex sign-in is not yet verified.**
Last assessed: October 19, 2026. This document is a release checklist, not a
working installation recipe. Start with [the current Codex guide](codex.md)
for local examples and its explicit connection limitations.

## Intended customer experience

1. Add ML Referee using the exact published Codex command or supported UI steps.
2. Sign in to an ML Referee account in the browser and authorize access.
3. Return to Codex and successfully check connection, access status, and credits.
4. Request beta access if needed; wait for operator approval, then recheck credits.

Customers must not create Auth0 applications, visit an administrator dashboard,
obtain a shared client secret, or copy tokens by hand. An ML Referee password is
not an email-mailbox, Auth0-administrator, or ChatGPT password. Use the account's
actual sign-in method; matching email text across providers does not prove a
shared service identity.

## What has been checked

- Codex CLI 0.144.4 locally exposes `--oauth-client-id` and `--oauth-resource`
  on `codex mcp add`, and supports `codex mcp login`.
- Public authorization discovery advertises S256 PKCE, public-client token
  authentication (`none`), refresh grants, and issuer-bound responses. It does
  not currently advertise automatic client registration through DCR or CIMD.
- These are capability observations, **not evidence of a successful Codex login**.
  An existing ChatGPT or Claude connection does not establish native Codex support.

## Publisher-side work

The candidate design is a dedicated public/native OAuth client for Codex, using
authorization code with S256 PKCE and no distributed application secret. Confirm
provider support before choosing it; do not repurpose the existing confidential
ChatGPT or hosted Claude client.

Publisher responsibilities:

- Obtain approval for identity-provider changes and record them privately.
- Establish the client, exact redirect matching, least-privilege user-delegated
  permissions, consent, audience, and a defined refresh rotation/expiry policy.
- Verify the actual callback emitted by the tested Codex version. Resolve
  loopback-port behavior explicitly; do not guess a callback or allow broad
  wildcard redirects. Preserve PKCE and issuer validation.
- Check that the resource parameter produces the intended API audience and
  that the required API and refresh scopes are actually granted.
- Keep existing ChatGPT/Claude clients, schemas, and submissions unchanged.
  Do not enable tenant-wide dynamic registration merely to bypass a failure.
- Keep credentials, raw tokens, account identifiers, authorization URLs, and
  operator deployment/configuration evidence out of this public repository.

Creating this checklist does not authorize production or identity-provider edits.
The candidate design is not final until the fresh-connection tests below pass.

## Acceptance tests

Run with an isolated test connection so existing working sessions are preserved.
Record the exact Codex version, operating system, and surface tested. CLI,
desktop, and remote execution environments must not inherit one another's pass.

| Check | Required evidence | Status |
| --- | --- | --- |
| Fresh setup | Exact install command or UI steps work without prior Referee tokens or a client secret | Pending |
| Browser sign-in | Correct ML Referee account signs in and consent returns successfully to Codex | Pending |
| Authenticated tools | Discovery and readiness calls succeed; an MCP server merely appearing in a list is insufficient | Pending |
| Beta request | With explicit permission, a request returns pending status and a private request identifier, without an evaluation | Pending |
| Approval and credits | Operator approves the intended account; a later readiness call shows the actual allocation | Pending |
| Token refresh | A real refresh exchange and subsequent authenticated call succeed without reconnecting | Pending |
| Existing integrations | Read-only ChatGPT and Claude checks still succeed without changed permissions or balances | Pending |

Do not spend evaluation credits merely to test sign-in. Do not shorten shared
token lifetimes, revoke other sessions, grant credits to the wrong account, or
treat token issuance as proof of refresh. Any separate evaluation requires its
own upload and quote approval.

## Troubleshooting to verify before publication

These are diagnostic categories, not observed error messages. Capture sanitized
messages from the actual rehearsal; never invent text and label it tested.

| Symptom | Diagnostic direction |
| --- | --- |
| Client registration fails | Confirm the dedicated client configuration; do not ask the customer to create an Auth0 app |
| Callback is rejected or browser cannot return | Compare the emitted callback, registered callback, listener port, and execution host |
| Login succeeds but a tool returns unauthorized | Check audience, granted scopes, issuer validation, and the intended connection |
| Connected but no credits | Check beta approval separately from authentication; do not retry evaluations |
| Session stops working later | Inspect refresh behavior privately; do not request tokens in support messages |

## Publish the verified guide

After the required checks pass, update `docs/codex.md` in the same repository:

- Replace `CONFIRMED_MCP_URL` with the tested connection instructions and any
  required public client identifier/configuration. Never include a client secret.
- Include the browser flow, expected readiness response, beta request and
  approval steps, and observed troubleshooting messages with sensitive fields removed.
- Publish the test date, minimum tested version, supported surface/platform,
  and remaining limitations. Keep unsupported surfaces explicitly pending.
- Record a sanitized pass/fail summary here. Keep raw provider logs, reviewer
  credentials, account/request IDs, and tokens in private operator records.
- Run repository checks and review the exact staged files and commit identity
  before pushing. Use the configured GitHub no-reply email.

Until then, local data preparation is usable, but direct Codex authentication
must not be advertised as ready for ordinary customers.

## References

- [Official Codex MCP guide](https://developers.openai.com/codex/mcp)
- [Official Codex configuration reference](https://developers.openai.com/codex/config-reference)

The official guides document pre-registered clients, OAuth callbacks and resource
configuration. They describe platform capabilities, not a tested ML Referee setup.
