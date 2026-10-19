# Practice with ML Referee

Start with data you can inspect, a question you can explain, and a budget you
control. These examples prepare inputs locally. They do not upload anything or
spend credits automatically.

| Example | What you learn | Needs a Referee account? |
| --- | --- | --- |
| [Synthetic regression](synthetic-regression/README.md) | Read a small dataset, declare a baseline and one candidate, follow the evaluation workflow | Not for local checks; yes for hosted evaluation |
| [Bike-demand forecasting](bike-demand/README.md) | Download licensed real data, construct six candidates without using same-hour observations, reserve later data | Not for preparation; yes for hosted evaluation |
| [Report integrity](report-integrity/README.md) | Hash an issued report locally and compare with its receipt | Local hashing does not; service verification does |

For Tom and other Codex users: [start here](../docs/codex.md). Claude users can
use the same staged prompts after connecting through a supported client; see
[integration status](../docs/claude.md). Prompts are instructions to your agent,
not an installer or a substitute for a working authenticated connection.

## The common workflow

1. **Prepare locally.** Inspect the data and define what the prediction is for.
2. **Discover and connect.** Check live schemas, beta approval, and usable credits.
3. **Authorize upload.** Send only the reviewed file, run preflight, obtain a quote.
4. **Approve the actual quote.** Submit that evaluation once, not an open-ended search.
5. **Read the evidence.** What is supported? What remains uncertain? Where would
   more data or a different candidate help answer the question?
6. **Save and follow up.** Preserve the actual report before expiry. Validate a
   chosen change on later data before making deployment decisions.

No hosted performance result is supplied or promised. The synthetic example is
a workflow exercise, not product evidence; the public-data example is not a
claim that every candidate will help. The scripts do not implement Referee's
evaluation engine.

## Before you start

- Python 3.10 or newer; only Python's standard library is needed.
- Git to clone this repository; internet access only to download public data
  and, separately, to use the hosted service.
- Read the [data and consent rules](../docs/usage.md). Public does not necessarily
  mean non-personal or licensed for reuse.
- Keep `data/` and `outputs/` local. Do not commit datasets, reports, receipts,
  audit identifiers, credentials, or signed links.

Run all local tests from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_public_repo.py
```

## If something goes wrong

| Situation | Next step |
| --- | --- |
| Python not found | Install Python 3.10+; on Windows use `py -3` in place of `python3` |
| Public download checksum changes | Stop; do not replace the pinned checksum just to pass the check |
| Python reports `CERTIFICATE_VERIFY_FAILED` | Repair Python's trusted certificate store, or use `--ca-file` with an administrator-approved CA bundle; never disable TLS verification |
| Output folder already exists | Choose a new `--output outputs/bike-demand-v2` folder; keep earlier artifacts |
| No Referee tools in your agent | Complete the local steps; use the connection guide or contact support |
| Sign-in succeeds but credits are unavailable | Check readiness; beta approval is separate and manual |
| Schema or preflight rejects the contract | Read the failure, propose a justified correction, get approval for scope changes |
| Submission times out | Recover the existing audit by its ID before submitting anything else |
| Report has expired | Say it expired; do not fabricate a result or automatically spend credits rerunning it |

[Support](https://mlreferee.com/support) can help with access. Never send passwords,
tokens, OAuth secrets, private datasets, or unredacted tool transcripts.
