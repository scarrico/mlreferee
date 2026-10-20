# Practice with your coding agent

Use ML Referee from your development workspace, with the coding agent you prefer.
These walkthroughs cover Codex and GitHub Copilot in VS Code, not browser-chatbot
integrations. The same files and staged prompts work without an agent, too.

## Start locally: no Referee account required

```sh
git clone https://github.com/scarrico/mlreferee.git
cd mlreferee
python3 scripts/practice.py
```

Python 3.10+ and Git are sufficient. On Windows, use `py -3` instead of `python3`.
The practice command checks the synthetic evaluation input, exercises the
public-data preparation tests with synthetic test records, and demonstrates
fingerprint checking. It makes no network requests or Referee calls. A passing
check is not a statistical evaluation or a working service connection.

Choose your workspace guide:

- [Codex desktop or CLI](codex.md)
- [GitHub Copilot in VS Code](copilot.md)
- [Run the examples yourself](../examples/README.md)

Paste this into your coding agent to begin:

> Read AGENTS.md and docs/coding-agents.md. Run python3 scripts/practice.py.
> Explain the outcome, baseline and candidate in the synthetic example. Tell
> me what passed locally and what still needs the hosted service. Do not change
> authentication settings, upload data, request access, or spend credits.

## Three exercises, one workflow

| Exercise | Do locally | Once an authenticated connection is verified |
| --- | --- | --- |
| [Synthetic regression](../examples/synthetic-regression/README.md) | Inspect 400 made-up rows; check one candidate against a declared baseline | Authorize upload, review preflight and quote, then approve one evaluation |
| [Bike-demand forecasting](../examples/bike-demand/README.md) | Download the pinned public UCI archive; prepare six candidates and reserve later data | Evaluate only the declared family; keep the holdout out of the first upload |
| [Report integrity](../examples/report-integrity/README.md) | Learn how a changed byte changes a fingerprint | Compare original issued report bytes with the actual verification record |

The report-hashing exercise demonstrates integrity, not correctness or safety.
The examples include no fabricated hosted results. Local preparation is useful
even while service access is pending.

## Connection status — October 20, 2026

| Client or component | Verified here | Still needed |
| --- | --- | --- |
| Shared Python exercises | Local checks and preparation tests | Hosted preflight and evaluation under separate authorization |
| Synthetic regression through Codex 0.163.0's managed MCP connection | Upload, valid preflight, approved one-credit submission, completion, result/receipt retrieval and locally hashed report-text verification | Model-driven conversation and original result-JSON byte download/verification |
| Public UCI bike data | Pinned archive verified; 7,920 evaluation rows, 672 reserved rows and six candidates prepared and structurally checked | Live schema, preflight and approved evaluation |
| Codex CLI 0.163.0 on local macOS | Fresh OAuth login; actual discovery/readiness and the synthetic evaluation workflow through Codex's app-server; separate model-driven discovery | Refresh, completed model-driven readiness (interactive elicitation was declined by the bounded harness) and new-account signup |
| Codex CLI 0.144.4 | Sign-in rehearsal failed due to resource handling | Use the tested 0.163.0 recipe, not this older version |
| Codex desktop | Workspace walkthrough written | Separate fresh-connection rehearsal; CLI results do not establish desktop compatibility |
| GitHub Copilot 0.65.0 in VS Code 1.137.0 on macOS, native HTTP connection | First browser sign-in and actual authenticated MCP calls; connected, authorized, ready | Native refresh, new-account onboarding and a complete authorized evaluation |
| Same Copilot setup with optional mcp-remote 0.15.1 helper and local file adapter | Two real refresh exchanges with rotation; protected calls after each and through Copilot after restart; model-driven synthetic upload/preflight, approved one-credit evaluation, report/receipt retrieval and local report-text SHA verification | New-account onboarding, other evaluation paths, natural-expiry scheduling and long-running sessions |

No directory approval, free-tier entitlement, or universal client compatibility
is implied. Your coding-agent subscription and Referee beta credits are separate.
A dedicated public Codex client is configured; follow the exact
[tested CLI connection recipe](codex.md). Copilot has its own
[tested first-login recipe](copilot.md) and an optional
[tested refresh helper](copilot.md#copilot-refresh-helper-tested-alternative).
The helper adds third-party software and a local JSON credential store, not an
OS keychain. Review its security notes before choosing it. Native Copilot and
Codex refresh remain unverified; the helper's bounded test does not establish
natural-expiry renewal or multi-day endurance.
Users do not need an Auth0 administrator account or a shared application secret.
See the [sign-in acceptance checklist](codex-auth-readiness.md).

## From connected to evaluated

### New customer checklist

These are the intended onboarding steps, not a claim that a fresh-account
rehearsal passed. They apply after choosing one of the client-specific recipes:

1. Sign into the coding client using your own client-provider account. Referee
   is a separate service account; do not use an email-mailbox password or an
   Auth0 administrator account for Referee.
2. Trigger the protected Referee connection check. On the Referee browser page,
   use **Log in** for an existing account or the offered signup flow for a new
   one. Complete any email verification or consent yourself. Never give the
   agent your password, verification link, client secret or token.
3. Check live readiness and credits. Connected does not mean beta-approved.
   If a different account is shown, stop and use the client's supported
   account-switch/reconnect flow; matching email strings do not prove identity.
4. If access is pending, explicitly ask the agent to request beta access once
   for candidate feature evaluation. Keep its request ID privately. A pending
   request is not a credit allocation, an evaluation, or proof an email was sent.
   Recheck that request's status rather than creating duplicate requests.
5. Wait for human approval, or redeem an invitation you actually received using
   the live tool. Do not invent invitation codes or assume a default credit grant.
   Recheck readiness, available credits and their returned expiration date.
6. Start the staged synthetic example only when ready. Review upload separately
   from the actual quote and evaluation authorization.

If signup, email delivery or account switching fails, contact
[support](https://mlreferee.com/support). Share only the client/version and a
sanitized error; provide a request ID privately if support needs it. Do not
publish identities, tokens, complete logs, or verification/transfer URLs.

### Evaluation checklist

1. **Prove the connection.** Call live read-only discovery and readiness tools.
   Inspect the returned tool output; an agent's plausible explanation is not proof.
2. **Check access.** Sign-in is not beta approval or a credit allocation. Request
   access only with permission, wait for approval, then recheck credits.
3. **Review the inputs.** Compare the example contract with the current schema.
4. **Approve upload only.** Use the example's staged prompts to get preflight
   and a quote. Keep the reserved holdout and unrelated files local. If the agent
   places raw CSV text into a tool argument, compare its exact decoded bytes to
   the original file before approval; row counts alone do not establish identity.
   The [Copilot rehearsal](copilot.md#synthetic-upload-rehearsal-stopped-before-transmission)
   caught a mismatch and stopped before upload; its subsequent local file adapter
   preserved the original bytes. The October 20 continuation passed the approved
   evaluation, report/receipt retrieval and report-text verification as well.
5. **Approve the displayed quote.** Submit once within that scope and cost.
6. **Read and preserve the result.** Explain what the evidence supports and where
   more data or further research might help. Save artifacts before expiration.

### Recovery and stop conditions

- **No tools or unauthorized:** stop hosted actions; use the selected client's
  sign-in instructions. Do not change Auth0 or borrow another client's secret.
- **Preflight invalid:** report the actual errors. Do not loosen the contract,
  change the candidate family or alter error targets to manufacture a pass.
- **Timeout after upload, quote or submission:** keep returned IDs and reuse the
  same operation key where the live tool supports one; do not invent an
  idempotency field. Recover the existing operation/status before any retry.
  If an upload tool has no retry key and its outcome is ambiguous, stop instead
  of blindly uploading again. Ask support if the outcome cannot be established.
- **Queued or running:** poll the existing job at reasonable intervals. A queue
  acknowledgment is not a completed report. Stop on a terminal status.
- **Expired/deleted report:** use a retained receipt if available, but do not
  claim it reconstructs the report. A new evaluation requires new authorization.
- **Hash mismatch:** check original bytes and representation; never paste the
  expected digest back as the candidate or interpret mismatch alone as fraud.

After saving the result and receipt privately, you may separately authorize
deletion of the exact owned audit/input. Retained fingerprints and necessary
metadata are distinct from report contents; deletion is not complete account
erasure. See the live service privacy policy and contact support for erasure.

If authentication fails, stop the hosted steps and contact
[support](https://mlreferee.com/support). Send the client version and a sanitized
error, never passwords, tokens, authorization URLs, datasets or raw transcripts.
