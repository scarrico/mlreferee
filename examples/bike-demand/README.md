# Which clues deserve a place in a bike-demand forecast?

A city needs enough rental bikes available each hour. Yesterday's demand at the
same hour is a reasonable starting clue. Would last week's demand, the time of
day, weekends, or earlier weather add useful evidence?

This walkthrough turns public city-level observations into a declared baseline
and six candidates for Referee. It prepares a real dataset without revealing
Referee's implementation or assuming which candidates will win.

## 1. What you need

Python 3.10+, this repository, and internet access for the initial download.
No Python packages, Node.js, Referee account, or credits are needed to prepare
the files. A hosted run additionally needs an authenticated supported connection,
beta approval, usable credits, and separate upload/submission authorization.

The source is **Seoul Bike Sharing Demand**, UCI dataset 560: hourly aggregate
rental counts with weather and calendar information. The reviewed CSV contains
no rider-level records or personal identifiers. It is licensed CC BY 4.0, not
under this repository's MIT license. See [source and attribution](SOURCE.md).

## 2. Download and prepare locally

Run from the repository root:

```sh
python3 examples/bike-demand/prepare.py download
python3 examples/bike-demand/prepare.py prepare
python3 scripts/check_example.py outputs/bike-demand/evaluation.csv outputs/bike-demand/contract.json
```

The first command downloads from UCI and checks the pinned archive fingerprint.
The second verifies the contained CSV and does not make network calls. It refuses to overwrite
an existing output folder. If starting another preparation, pass
`--output outputs/bike-demand-v2` and use that path in subsequent commands.

Expected local output:

```text
Prepared 7920 evaluation rows, 672 reserved rows, 6 candidates.
```

If a macOS Python installation lacks its certificate bundle, install its trusted
certificates or explicitly use the system CA bundle, if present:

```sh
python3 examples/bike-demand/prepare.py download --ca-file /etc/ssl/cert.pem
```

On other systems use your administrator-approved bundle. Never bypass certificate
verification. An already downloaded archive is rechecked, not downloaded again.

| File | Purpose |
| --- | --- |
| `data/seoul-bike.zip` | Original source archive, ignored by Git |
| `outputs/bike-demand/evaluation.csv` | The only data file proposed for the first upload |
| `outputs/bike-demand/contract.json` | Draft column roles and validation settings, based on the published general-ML fixture |
| `outputs/bike-demand/holdout.csv` | Final 28 days, reserved for later validation; do not upload in the first run |
| `outputs/bike-demand/manifest.json` | Source, license, hashes, transformations, assumptions, and row counts |

Local checks inspect structure and timing order. They are not the hosted
preflight, a guarantee against leakage, or a determination of legal compliance.
The prepared contract must be checked against the live schema before upload.

## 3. Understand the spreadsheet

Each row is one hour for the Seoul system. At the **start** of that hour, predict
the total rentals during that hour. Rows are in chronological order.

| Column | Role and availability |
| --- | --- |
| `outcome` | Rentals during the target hour; this is the answer, never an input clue |
| `observation_time` | Start of the target hour, explicitly UTC+09:00 |
| `label_available_time` | Target-hour start plus two hours; an explicit exercise assumption |
| `entity` | Constant `seoul_system`; identifies the aggregate system, not a rider |
| `demand_lag_24h` | Baseline input: rentals in the hour 24 hours earlier |
| `demand_lag_48h` | Candidate: rentals 48 hours earlier |
| `demand_lag_168h` | Candidate: rentals in the corresponding hour a week earlier |
| `hour_sin`, `hour_cos` | Two calendar candidates encoding the daily cycle; together with the other four, six submitted columns |
| `weekend` | Calendar candidate known before the forecast |
| `temperature_lag_24h` | Candidate: measured temperature 24 hours earlier, not future weather |

The baseline is a **feature set**, not supplied out-of-fold predictions or a
production model. This example follows the public regression contract with
expanding chronological validation, five folds, and a two-hour embargo.
The template's `train_window=1440` is ignored for this expanding split. That
setting applies only to rolling validation and counts distinct observation
timestamps, not rows or elapsed time. It does not limit this example to 1,440
training rows. Ask the live schema to confirm how settings apply; do not treat
the local template as a current API guarantee.

### Timing is part of the experiment

The source does not provide actual ingestion/publication timestamps. We assume
the count and weather for an hour are available two hours after that hour begins
(one hour for the interval to finish and one for reporting). The lagged inputs
are at least 24 hours old. This assumption is **not** a measured source guarantee;
replace it with actual availability evidence for your own system.

We exclude measured same-hour weather, which would not yet be known at prediction
time. We retain all hours, including periods when the rental system was not
functioning, so the target is **observed rentals**, not unconstrained customer
demand. Closure effects may matter. We do not use the source's functioning-day
flag as a predictor because its advance availability is not established here.

The first 168 rows supply lag history and are not evaluated. The final 672 rows
are withheld. During any later sequential hourly holdout test, earlier holdout
outcomes may become available for lagged inputs; this is not a single forecast
made 28 days ahead. Reserve the holdout until a follow-up plan is agreed.
At each later validation cutoff, fit only on outcomes whose declared availability
precedes that cutoff; respect the reporting delay at the evaluation/holdout
boundary too. The preparation script creates files, not a downstream training loop.

## 4. Have Codex or another agent guide the hosted run

Open [the staged prompts](prompts.md). First explain and review the files, then
discover current tools and the `general_ml` schema. Stop if the client cannot
connect. You can still complete all the local steps.

Once connected, authorize uploading **only `evaluation.csv`** with its reviewed
contract. The agent should run free preflight, resolve failures without hiding
them, obtain a quote, and stop. Review the scope and actual credit cost before
authorizing that one submission. Do not assume a fixed price from this example.

The tool sequence is discovery/readiness → schema → authorized upload →
`preflight_dataset` → `quote_audit` → approved `submit_audit` → status → result.
Use the current tool schemas for arguments; this guide does not invent an HTTP
request body or an upload endpoint. Six candidates fit the single-audit pattern;
larger families require discovery of the service's current campaign rules.

## 5. Use the answer to decide what to investigate next

Read the actual report, not the apparent correlation in a spreadsheet. Ask:

- Which candidates add evidence beyond yesterday's same-hour demand?
- Which remain uncertain, and is that uncertainty concentrated in particular periods?
- Would additional seasons, closure information, or better-timed weather data
  make a useful next experiment? These are hypotheses to investigate, not
  promises that more data will resolve a result.
- What downstream validation should precede a change to bike allocation?

The two hour-cycle columns do not establish a joint interaction result merely
because both were submitted. Do not repeatedly change the family until one
result looks favorable. Declare subsequent searches and preserve earlier results.

Save the returned report and receipt before expiry. Later, use the reserved
period for a predeclared downstream check under a separate authorization. A
single year in one city does not establish generalization to other cities,
seasons, or operational policies. This repository includes no hosted result
and makes no claim that the example improves a deployed forecasting system.
