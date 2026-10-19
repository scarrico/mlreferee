# Suggested agent prompts

Use these separately, observing the returned state before continuing.

## 1. Discover and check access

> Discover ML Referee's current capabilities and schemas, then check my access
> and credit balance. Do not upload data, request beta access, redeem an invite
> or submit an evaluation. Tell me what prerequisites are missing.

## 2. Prepare the synthetic input

> Use only this repository's synthetic regression example.csv and contract.json.
> Explain the objective, outcome, baseline, complete candidate family, timing,
> grouping and validation plan. Check the current input schema and flag any
> incompatibility. Do not upload or run anything yet.

## 3. Authorize upload, preflight and quote only

> I authorize uploading this synthetic fixture to ML Referee for the declared
> evaluation, running preflight and obtaining a quote. Show me the returned
> scope, retention window and credit cost. Stop before submitting an evaluation.
> Do not weaken the contract to make preflight pass.

## 4. Submit only after seeing and accepting the actual quote

> I authorize this specific quoted evaluation at the cost you just showed me.
> Submit it once, recover retries by their identifiers, and retrieve the completed
> result. Do not run additional experiments or spend beyond this quote.

## 5. Save and interpret

> Explain the measured effect, uncertainty, adjusted evidence, fold stability
> and limitations. Preserve the feature-quality-only scope. Help me save the
> original report and receipt before expiry. If current tools cannot download
> the original bytes, say so. Do not reconstruct JSON and claim its file hash
> matches. Do not delete the report or input unless I explicitly ask.
