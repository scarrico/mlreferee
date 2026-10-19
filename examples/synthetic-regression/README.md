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

Do not replace observation time with label-availability time or submit a future
label as if it were known at prediction time. The contract uses expanding
validation with five folds and declares the complete one-candidate family.

The prompts deliberately stop for quote approval. No command in this example
automatically uploads data, requests beta access, purchases credits or submits
an evaluation. Read the quote rather than inferring a fixed price.
