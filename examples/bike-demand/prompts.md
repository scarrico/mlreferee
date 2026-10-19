# Bike-demand prompts for Codex and other agents

Run these stages separately. Read the result of each before authorizing the next.
Keep identifiers and outputs private; these prompts contain no credentials.

## 1. Local preparation only

> Read AGENTS.md and examples/bike-demand/README.md. Download the pinned UCI
> archive using prepare.py download, run prepare.py prepare, and run
> scripts/check_example.py on the evaluation CSV and contract. Explain the
> baseline, all six candidates, timestamps, reserved holdout, source license,
> and assumptions. You may write to data/ and outputs/ locally. Do not upload
> to Referee, change account settings, or spend credits. If files already exist,
> preserve them and ask before changing the experiment.

## 2. Read-only service readiness

> Discover current Referee tools and check readiness and credits. Fetch the
> general_ml input schema and compare it with outputs/bike-demand/contract.json.
> Report any mismatch and proposed correction before changing scope. Do not
> request beta access, redeem an invite, upload data, or submit anything.
> If authentication or tool access fails, stop the hosted workflow and explain.

## 3. Upload approval, preflight and quote — not submission

> I approve uploading only outputs/bike-demand/evaluation.csv to ML Referee
> with the reviewed contract for the bike-demand evaluation. Confirm the file
> hashes against manifest.json first. Do not upload holdout.csv, other local
> files, credentials, or transcripts. Run preflight and obtain a quote using
> current schemas. Show the actual cost, scope, expiry, and any warnings.
> Stop before submission. Do not silently drop candidates, weaken validation,
> or alter evidence thresholds to make the request pass.

## 4. Explicit approval of the displayed quote

Use this only after reviewing the returned quote. Replace the placeholders
with the actual values shown privately by your agent:

> I authorize quote [QUOTE ID] for [COST] credits, for exactly the displayed
> bike-demand family and contract. Submit once. Preserve the returned identifiers
> and reuse the appropriate idempotency key on a retry of the same request.
> If the quote changes or expires, stop for new approval. Recover status after
> a timeout rather than creating another evaluation. Retrieve the actual
> completed result; do not launch follow-ups or exceed this cost.

## 5. Interpret, preserve and propose next research

> Save the actual result and receipt using the available supported mechanism
> before expiry, under outputs/ with no public commit. Distinguish original
> report bytes from a saved tool response. Explain supported, provisional,
> unresolved and no-incremental-evidence findings using the report's own values.
> What does this suggest keeping, reconsidering, or investigating with more
> data? Do not discard an uncertain feature just because the evidence is
> inconclusive. Propose a predeclared later-data validation plan without running
> it or inspecting holdout outcomes to choose candidates. This is feature-quality
> evidence, not a deployment recommendation or guarantee. Do not delete artifacts
> unless I ask.
