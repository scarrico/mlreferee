# Accounts, data and interpretation

For a guided first run, see [practice examples](../examples/README.md) and
[the Codex walkthrough](codex.md). Local preparation needs no service account.

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
