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

## Connection status — October 19, 2026

| Client or component | Verified here | Still needed |
| --- | --- | --- |
| Shared Python exercises | Local checks and preparation tests | Hosted preflight and evaluation under separate authorization |
| Public UCI bike data | Pinned archive verified; 7,920 evaluation rows, 672 reserved rows and six candidates prepared and structurally checked | Live schema, preflight and approved evaluation |
| Codex CLI 0.163.0 on local macOS | Fresh OAuth login; actual discovery and readiness through Codex's app-server | Refresh and a complete authorized evaluation; new-account signup |
| Codex CLI 0.144.4 | Sign-in rehearsal failed due to resource handling | Use the tested 0.163.0 recipe, not this older version |
| Codex desktop | Workspace walkthrough written | Separate fresh-connection rehearsal; CLI results do not establish desktop compatibility |
| GitHub Copilot 0.65.0 in VS Code 1.137.0 on macOS | First browser sign-in and actual authenticated MCP calls; connected, authorized, ready | Persistent sign-in/refresh, new-account onboarding and a complete authorized evaluation |

No directory approval, free-tier entitlement, or universal client compatibility
is implied. Your coding-agent subscription and Referee beta credits are separate.
A dedicated public Codex client is configured; follow the exact
[tested CLI connection recipe](codex.md). Copilot has its own
[tested first-login recipe](copilot.md); refresh remains unverified for both.
Users do not need an Auth0 administrator account or a shared application secret.
See the [sign-in acceptance checklist](codex-auth-readiness.md).

## From connected to evaluated

1. **Prove the connection.** Call live read-only discovery and readiness tools.
   Inspect the returned tool output; an agent's plausible explanation is not proof.
2. **Check access.** Sign-in is not beta approval or a credit allocation. Request
   access only with permission, wait for approval, then recheck credits.
3. **Review the inputs.** Compare the example contract with the current schema.
4. **Approve upload only.** Use the example's staged prompts to get preflight
   and a quote. Keep the reserved holdout and unrelated files local.
5. **Approve the displayed quote.** Submit once within that scope and cost.
6. **Read and preserve the result.** Explain what the evidence supports and where
   more data or further research might help. Save artifacts before expiration.

If authentication fails, stop the hosted steps and contact
[support](https://mlreferee.com/support). Send the client version and a sanitized
error, never passwords, tokens, authorization URLs, datasets or raw transcripts.
