# Synthetic regression walkthrough

This is an entirely synthetic, 400-row example with one baseline feature and
one candidate feature. It is the published general-ML fixture, not a customer
dataset or evidence of real-world predictive performance.

- [example.csv](example.csv): observations, label availability, synthetic entity,
  baseline, candidate and outcome.
- [contract.json](contract.json): published regression contract.
- [prompts.md](prompts.md): discovery, preparation, quote and authorization steps.

The fixture source is
[the service's published example](https://api.mlreferee.com/public/verticals/general_ml/example.csv)
and [contract](https://api.mlreferee.com/public/verticals/general_ml/contract.json).
The local files are reviewed snapshots; use current tool discovery and live
schema constraints when preparing a request.

## Run the local check

From the repository root, with Python 3.10 or newer:

```sh
python3 scripts/check_example.py examples/synthetic-regression/example.csv examples/synthetic-regression/contract.json
```

Expected: 400 rows, one baseline feature, one candidate. No network call or
Referee account is required. The checker verifies declared columns, finite
numeric values, chronological rows per entity, and labels arriving later than
prediction time. It cannot certify the validity of arbitrary data or replace
live preflight.

## What using it looks like

The question is: **does `candidate` add predictive evidence beyond `baseline`
for `outcome`?** Each row is a made-up observation. `entity` groups observations;
`observation_time` is the prediction time; `label_available_time` says when its
answer becomes available. `outcome` must never be included among the predictors.
The baseline is an input feature here, not a supplied production model or score.

Open this folder in your coding agent and follow
[the Codex or Copilot guide](../../docs/coding-agents.md).
Then use [prompts.md](prompts.md) one step at a time: readiness and schema,
preparation, upload/preflight/quote approval, approval of the displayed quote,
then result retrieval. If no supported connection is available, stop after the
local exercise. Installing repository files is not beta approval.

After the run, the useful artifact is the actual Referee report: its comparison,
effect and uncertainty, finding, and limitations. There is no expected winning
result supplied here. A synthetic success is not evidence of real-world value.
Save reports privately in `outputs/`, not alongside this public fixture.

Next, try the [real bike-demand example](../bike-demand/README.md) to learn
source licensing, lagged inputs, multiple candidates, and reserved later data.

Do not replace observation time with label-availability time or submit a future
label as if it were known at prediction time. The contract uses expanding
validation with five folds and declares the complete one-candidate family.

The prompts deliberately stop for quote approval. No command in this example
automatically uploads data, requests beta access, purchases credits or submits
an evaluation. Read the quote rather than inferring a fixed price.
