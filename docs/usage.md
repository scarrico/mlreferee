# Accounts, data and interpretation

For a guided first run, follow [Start here](../README.md#start-here), then choose
[Codex](codex.md) or [GitHub Copilot in VS Code](copilot.md).
Local preparation needs no service account.

Start by asking your agent to check ML Referee access and credits without
uploading anything or submitting an evaluation. A plugin install, account
connection, beta approval and a usable credit balance are separate states.
Use the same ML Referee account and sign-in method across clients when you want
the same service identity. Matching email text alone does not establish identity.
Chat history does not transfer between applications.

Use only data you are authorized to submit. During beta, evaluation datasets
must be synthetic, non-personal or genuinely anonymized. Regulated datasets,
identifiable or pseudonymized person-level records, private prompts, credentials
and payment details are prohibited. The service is for adults doing business
or professional research. A local language model still sends authorized
evaluation data to the hosted service through the connector.

Declare the objective, outcome, baseline, candidate family, observation times,
label-availability times, grouping and validation plan before evaluation. Keep
the time of an observation distinct from when its label became available.
Discover the current tool schemas. Do not invent fields or silently weaken a
failed preflight.

Preflight does not submit an evaluation. A quote does not spend its quoted
credits; the agent must show scope and cost and obtain authorization before
submission. Reuse identifiers and idempotency keys to recover interrupted work
rather than accidentally creating another evaluation. Available credits are
not permission to run unrelated experiments.

Reports expire with their associated inputs, not a fresh window after completion.
Save the report and retained receipt before expiry. Minimal fingerprints and
necessary metadata can remain afterward; report deletion is not complete
account erasure. Follow the [privacy notice](https://mlreferee.com/privacy) and
use [support](https://mlreferee.com/support) for account/privacy requests.

Hash verification requires the original artifact and local byte hashing. A
digest match establishes consistency, not statistical correctness, safety, or
absence of harm; a mismatch may be formatting and does not prove fraud.

Referee provides feature-quality evidence within a declared evaluation setup,
not guarantees of future predictive performance, model safety, legal compliance
or deployment readiness. It does not recommend financial positions or
transactions. Bounded repairs require prospective confirmation on new labels.

The language model and the agent harness are separate. MCP support, OAuth,
file access and local hashing depend on the harness; a provider's model API
alone does not establish a working Referee integration.

## Troubleshooting

| What you see | What to do next |
| --- | --- |
| No tools, sign-in failure or expired session | Stop hosted actions. Follow the [Codex connection guide](codex.md#2-connect-codex-cli) or [Copilot connection guide](copilot.md#2-connect-referee-in-vs-code). Review any browser consent yourself. Do not borrow credentials, disable TLS checks or edit Auth0 settings. |
| Connected, but beta access is pending | Follow the [new-customer checklist](coding-agents.md#new-customer-checklist). Request access once with permission, then wait for human approval. Signup alone grants neither approval nor credits. |
| Insufficient or expired credits | Check the live balance and expiration, compare them with the current quote, and stop before submission. Contact support about access; do not assume a grant, purchase or refund. |
| Upload fails, its hash differs, or its outcome is unclear | Do not approve reconstructed or altered data. Check the original file and the client's supported file-upload path. If an upload may already have succeeded, recover its status before retrying; a matching row count is not proof of matching bytes. |
| Preflight rejects the input or contract | Read the actual errors. Correct only a justified preparation mistake, and get approval for any change to the declared evaluation. Do not relax evidence requirements just to pass. |
| Quote expires or submission times out | Before submission, obtain a current quote and reconfirm any changed scope or cost. After a possible submission, recover the existing job using its identifiers and supported retry key; do not create a replacement run blindly. |
| Report is expired or its fingerprint differs | A receipt cannot reconstruct expired report contents. Check the exact bytes and the selected [verification representation](../examples/report-integrity/README.md). Never use the expected receipt hash as your computed hash. Any rerun needs separate authorization. |

For a queued or running evaluation, check the existing job at reasonable
intervals; do not resubmit. See [recovery and stop conditions](coding-agents.md#recovery-and-stop-conditions)
for the staged workflow.

### Asking for help

Use the public [support form](https://mlreferee.com/support). Include:

- The coding client, version and operating system.
- The step that failed and a sanitized error message.
- Whether a job was submitted or the outcome is uncertain. Provide its request
  or audit identifier privately only if support needs it.

Never include passwords, OAuth secrets, access tokens, full authorization URLs,
raw logs or evaluation datasets. Use the same form for privacy or deletion
inquiries. Support requests do not authorize a new evaluation or credit spending.
