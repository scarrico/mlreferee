# Codex sign-in: implementation and verification process

Status: **partial acceptance: fresh Codex CLI login and authenticated tools passed;
refresh and a model-driven conversation remain unverified.**
Last assessed: October 19, 2026 (Pacific). Use [the tested CLI recipe](codex.md).
This checklist records what passed and what remains; it is not a claim that
every client surface or end-to-end example is ready.

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

- Official Codex CLI 0.163.0 on local macOS completed fresh credential acquisition
  for a dedicated public/native client. The browser already had an existing
  Referee account session; the user accepted new consent. New-account signup
  and password entry were not tested. The global CLI was not replaced.
- `describe_referee` and `get_referee_readiness` returned live connected/authorized
  status and existing credit availability through the official Codex app-server
  MCP tool-call interface, using Codex-managed OAuth credentials. This was not
  a manual token probe. No model-driven evaluation, upload, quote or credit use
  was tested. Account identifiers and balances are omitted from public evidence.
- Public authorization discovery advertises S256 PKCE, public-client token
  authentication (`none`), refresh grants, and issuer-bound responses. It does
  not currently advertise automatic client registration through DCR or CIMD.
- The configured rotating-refresh policy is seven days of inactivity and a
  30-day maximum. A configured policy and initial token exchange do not prove
  that a real refresh succeeds; that gate remains pending.
- Existing ChatGPT readiness passed. Public tool schemas remained unchanged;
  Claude authenticated access was not independently retested.

## Publisher-side work

A dedicated third-party Native public OAuth client was created with explicit
owner approval, authorization-code/PKCE, no distributed application secret,
and an exact fixed loopback callback. Only user-delegated Referee read/write
permissions and refresh were configured; machine-to-machine access is disabled.
Existing ChatGPT and Claude clients were not repurposed or changed.

Ongoing publisher responsibilities:

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

Future provider changes need their own authorization. Successful setup does not
close the remaining acceptance gates below.

## Acceptance tests

Run with an isolated test connection so existing working sessions are preserved.
Record the exact Codex version, operating system, and surface tested. CLI,
desktop, and remote execution environments must not inherit one another's pass.

| Check | Required evidence | Status |
| --- | --- | --- |
| Fresh setup | Exact pinned CLI/config recipe works without prior tokens for the new client or a shared secret | Passed: CLI 0.163.0, local macOS |
| Browser sign-in | Existing account SSO plus new consent returns successfully to Codex | Passed; new-account signup not tested |
| Authenticated tools | Discovery and readiness calls succeed through Codex's managed MCP connection | Passed via app-server tool-call RPC; no model-driven workflow tested |
| Beta request | With explicit permission, a request returns pending status and a private request identifier, without an evaluation | Pending |
| Approval and credits | Readiness shows the existing account's access and balance | Read passed; a new approval/grant was not tested |
| Token refresh | A real refresh exchange and subsequent authenticated call succeed without reconnecting | Pending |
| Existing integrations | Read-only checks succeed without changed permissions or balances | ChatGPT passed; Claude authenticated check pending; public schemas unchanged |
| Synthetic example | Approved upload, preflight, quote, submission and result retrieval | Passed via managed MCP tool calls: one credit; report and receipt retrieved; locally hashed report text returned digest_match. Model-driven conversation and original result-JSON byte verification remain untested |
| Other Codex surfaces | Desktop, IDE, other OS and remote execution rehearsals | Not tested; separate [Copilot first-login results](copilot.md) do not establish Codex compatibility |

Do not spend evaluation credits merely to test sign-in. Do not shorten shared
token lifetimes, revoke other sessions, grant credits to the wrong account, or
treat token issuance as proof of refresh. Any separate evaluation requires its
own upload and quote approval.

## Observed setup issues

- CLI 0.144.4 generated a trailing-slash resource that Auth0 did not recognize.
- An explicit `oauth_resource` override caused a duplicate resource parameter,
  including in 0.163.0. Omitting it allowed 0.163.0 to discover the exact resource.
- The first generated callback was unregistered. The dedicated client now has
  the exact callback and matching fixed listener port in the setup guide.
- Explicit scopes avoided the older CLI's unintended default profile scopes.

The categories below remain general diagnostic guidance, not additional observed
errors. Never publish account identifiers, tokens, or raw authorization URLs.

| Symptom | Diagnostic direction |
| --- | --- |
| Client registration fails | Confirm the dedicated client configuration; do not ask the customer to create an Auth0 app |
| Callback is rejected or browser cannot return | Compare the emitted callback, registered callback, listener port, and execution host |
| Login succeeds but a tool returns unauthorized | Check audience, granted scopes, issuer validation, and the intended connection |
| Connected but no credits | Check beta approval separately from authentication; do not retry evaluations |
| Session stops working later | Inspect refresh behavior privately; do not request tokens in support messages |

## Complete the remaining gates

There is no documented force-refresh MCP CLI/RPC action in this rehearsal.
Credentials are in the OS-managed store. Do not extract or modify them, revoke
sessions, or shorten shared token lifetimes to manufacture a refresh test.
Observe a natural-expiry refresh exchange and a subsequent authenticated call.
A manual token grant, if separately authorized, would not establish Codex-managed
refresh behavior.

When additional checks pass, update `docs/codex.md` in the same repository:

- Preserve the tested public client settings and exact recipe. Never include a secret.
- Add any newly verified beta-request, approval, refresh and full-example steps,
  with sensitive fields removed and untested steps still clearly identified.
- Publish the test date, minimum tested version, supported surface/platform,
  and remaining limitations. Keep unsupported surfaces explicitly pending.
- Record a sanitized pass/fail summary here. Keep raw provider logs, reviewer
  credentials, account/request IDs, and tokens in private operator records.
- Run repository checks and review the exact staged files and commit identity
  before pushing. Use the configured GitHub no-reply email.

The connection recipe is tested only to the scope stated above. Do not advertise
full workflow, automatic refresh, directory approval or broader client support
from the initial connection result.

## References

- [Official Codex MCP guide](https://developers.openai.com/codex/mcp)
- [Official Codex configuration reference](https://developers.openai.com/codex/config-reference)

The official guides document pre-registered clients, OAuth callbacks and resource
configuration. They describe platform capabilities, not a tested ML Referee setup.
