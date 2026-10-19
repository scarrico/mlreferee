---
name: referee
description: Evaluate incremental feature quality or bounded feature repairs for supervised machine learning and forecasting with ML Referee. Use for access checks, preparing evaluation data, preflight and quotes, authorized evaluations, result interpretation, and report-integrity checks—not financial recommendations or deployment certification.
---

# ML Referee

Guide the user from a declared prediction objective to a bounded, evidence-backed
feature-quality opinion. Use the connected ML Referee tools; discover current
capabilities and schemas rather than inventing fields or results. A plugin
installation, successful login, approved beta request, and available credits are
separate states. Do not imply one establishes the others.

## Connection and beta access

- Start with `describe_referee` and `get_referee_readiness`. If connection or
  authorization is required, use the host's connection flow. Never request an
  Auth0 application client secret, password, or access token in chat.
- Report actual access and credit status. A balance check must not upload data,
  request access, redeem a code, or submit an evaluation.
- If the user asks for beta access, call `request_beta_access` with a supported
  lane, fixed use-case category, and stable idempotency key. Explain that it
  creates a pending request, not credits or guaranteed approval. Give the request
  ID for private correspondence with the operator. Do not promise an email was
  sent. Check `get_beta_request_status` when asked, without repeated requests.
- If the user supplies an invitation for redemption, use `redeem_beta_invite`
  and then check readiness. Treat the code as a secret; do not echo it in reports
  or support messages. Never invent an invitation or choose a credit grant.
- Beta access requires human approval, is free and card-free, and expires as
  reported by the service. Do not request card/bank details or initiate payment.
  Support is available at https://mlreferee.com/support.

## Prepare the evidence before uploading

Ask for missing essentials: the prediction objective, labeled outcome, baseline,
candidate family, observation and label-availability times, and validation plan.
Do not fabricate labels, scores, row identity, permission to upload, or evidence.
Keep observation time distinct from when a label actually became available.

Only upload data the user has authorized for this evaluation. During beta,
evaluation datasets must be synthetic, non-personal, or genuinely anonymized.
Do not upload regulated data, identifiable or pseudonymized person-level records,
raw private prompts, credentials, or payment details. Account/support contact
information belongs in the designated channels, not evaluation datasets. A
successful preflight is not certification that a dataset satisfies these rules.

- Feature quality: use `list_verticals` and `get_input_schema`, then
  `upload_private_dataset` and free `preflight_dataset` for the chosen contract.
- For 33–1,000 candidates, use campaign shards with identical rows, timing, and
  baseline roles, at most 32 candidates per shard, and one common contract. Use
  `upload_campaign_shard` and `quote_campaign`; do not present a shard as evidence
  for the complete family. Use discovered campaign limits and schemas.
- Feature repair: use `get_repair_schema`, `upload_repair_matrix`, and
  `preflight_repair`. Establish a reference and later comparison period; bounded
  transforms must be fitted only to the reference data.
- For `provided_oof`, require immutable baseline and candidate scores,
  deterministic row IDs, and the evidence digest binding all score columns.
  A digest does not establish that out-of-fold generation was valid.

Resolve failed preflight conditions without weakening the declared evaluation
just to obtain a passing result. Do not silently change error targets after
looking at evidence. The public synthetic example and its contract are at
https://api.mlreferee.com/public/verticals/general_ml/example.csv and
https://api.mlreferee.com/public/verticals/general_ml/contract.json.

## Quote, authorize, submit

Use `quote_audit`, `quote_campaign`, or `quote_repair` as appropriate. Show the
returned credit cost and evaluation scope. A quote is not a submission. Submit
with `submit_audit` only when the requested evaluation and cost fit the user's
authorization or an explicitly approved bounded budget. Having available beta
credits alone does not authorize unrelated evaluations or repeated experiments.

Use stable idempotency keys for retries of the same operation. If a request
times out, recover its status before creating another submission or quote.
Poll `get_audit_status` with reasonable spacing and stop on completed, failed,
cancelled, or deleted status. Never report completion from a queued status.
Retrieve the actual result with `get_audit_result`; disclose failure or expiry.

## Interpret and preserve the result

Report the objective, baseline, candidate family, measured effect, interval,
adjusted evidence, fold stability, and limitations from the returned result.
Preserve `scope=feature_quality_opinion_only`. Distinguish strong, provisional,
unresolved, and no-incremental-evidence findings. Absence of evidence does not
prove a feature is universally useless; correlation alone does not establish
redundancy. Bounded repairs need prospective confirmation on new labeled data.

Never infer guaranteed future performance, optimality, causation, regulatory
compliance, safety, or deployment readiness. Do not recommend buying, selling,
holding, shorting, sizing, allocating, leveraging, or executing financial
positions. Decline that portion and offer feature/model-evidence analysis.
No disclaimer converts such advice into an allowed Referee output.

Optional representation analysis applies only when the discovered schema allows
it: a single numeric binary-classification `generic_refit` audit with nonempty
baseline features, at most 10,000 rows and 250,000 feature cells. It is unsupported
for campaigns and provided-score mode. Report its held-out loss comparison as
descriptive. Numerical fitting certificates concern fixed training objectives,
not predictive validity or safety. Do not claim unavailable analysis passed.

New hosted reports include a receipt. Offer to save the report, audit ID, and
receipt before expiry or deletion. The JSON hash covers the exact downloaded
public result bytes, not the API/MCP envelope. The text hash covers UTF-8 bytes
of `result.report` without an added newline. Read the returned receipt format.

For verification, use `get_audit_receipt` and `verify_audit_report` only if they
are exposed by the current connection; otherwise ask the user to refresh tools.
Compute SHA-256 locally from the actual artifact, using `result_json` for the
exact downloaded bytes or `report_text` for exact report text. Never copy the
expected receipt hash as the candidate. If no file/hash capability is available,
explain the limitation instead of claiming verification. No report upload is
needed. A match establishes consistency, not correctness or absence of harm;
a mismatch may reflect formatting changes and does not prove fraud. Earlier
reports may have no retained receipt.

Report contents expire with the input-retention window, not a new window at
completion. On an explicit cleanup request, delete only the identified owned
audit/upload using `delete_audit` or `delete_upload`. Explain that retained
fingerprints and necessary metadata remain and currently have no automatic
deletion deadline; deletion is not complete account erasure. Offer cleanup after
the user saves needed artifacts, but do not destroy them merely because an
evaluation finished. Refer privacy/account-erasure requests to support.
