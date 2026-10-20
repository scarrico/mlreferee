# Use ML Referee examples with Codex

You can use Codex to prepare the files, explain their columns, and guide an
authorized evaluation. You do not need to write an API client to try the local
examples. A local folder alone does not give Codex access to ML Referee.

## 1. Open the repository

```sh
git clone https://github.com/scarrico/mlreferee.git
cd mlreferee
```

In the Codex desktop app, open this folder and start a task in it. In the CLI,
run `codex` from this directory. Codex should read `AGENTS.md` before working.
Do not open the private service repository or give the agent unrelated data.

Paste this first:

> Read AGENTS.md, examples/README.md, and examples/bike-demand/README.md.
> Walk me through the bike-demand example. You may download the pinned public
> UCI archive and run the local preparation and checks. Do not upload data to
> ML Referee, request beta access, redeem invitations, submit evaluations,
> change connection settings, or spend credits. Show me the exact files,
> candidate list, timing assumptions, and remaining prerequisites. Stop there.

For a smaller first exercise, substitute `examples/synthetic-regression/README.md`
and ask it to use the included fixture without any download.

## 2. Check whether Codex can actually call Referee

The [versioned sign-in readiness checklist](codex-auth-readiness.md) tracks the
publisher-side work and fresh-connection tests still needed. It is not yet a
tested end-to-end installation guide.

If ML Referee is already connected, ask:

> Use ML Referee's read-only discovery and readiness tools. Check the current
> input schema for general_ml and my submission readiness. Do not request beta
> access or upload anything. If tools are absent or authentication fails, explain
> that limitation; do not invent an HTTP call or use someone else's credentials.

For a direct MCP connection, use the endpoint and sign-in instructions supplied
for **your approved Codex client**. This repository has not established that
arbitrary Codex OAuth clients can sign in. The Claude preview configuration is
not proof of Codex compatibility, and a submitted ChatGPT integration is not a
publicly approved release. Ask [support](https://mlreferee.com/support) if you
have not been given a supported connection path.

For reference, Codex's generic CLI setup looks like this **after you have a
confirmed endpoint**; replace the placeholder, do not run it literally:

```sh
codex mcp add mlreferee --url 'CONFIRMED_MCP_URL'
codex mcp login mlreferee
codex mcp list
```

In the CLI's interactive session, `/mcp` shows active MCP servers. Use the normal
browser sign-in flow; never paste passwords, access tokens, or application
secrets into a prompt or this repository. Do not change OAuth settings to make
an unsupported connection work.

Connection controls can vary by Codex surface. See the
[official MCP guide](https://developers.openai.com/codex/mcp) for current setup.
These commands are configuration guidance, not a tested Referee sign-in recipe.

## 3. Run the example in deliberate stages

Use the [bike-demand prompts](../examples/bike-demand/prompts.md) or
[synthetic prompts](../examples/synthetic-regression/prompts.md) one at a time.
They separate permission to upload from permission to spend credits. Do not
paste all stages together as one instruction.

Before submission, you should see:

- The outcome and prediction time, baseline, full candidate family, and validation plan.
- The exact CSV and contract being uploaded; the reserved holdout is excluded.
- The live preflight response and a quote with its scope and actual credit cost.
- A request for your explicit approval of that quote.

After submission, ask Codex to save what the live tools actually return in your
local `outputs/` folder, explain the result in plain language, and propose next
research steps. Saving a rendered MCP response is not the same as downloading
the original report bytes. Use the [integrity guide](../examples/report-integrity/README.md)
only with the correct original artifact.

## 4. A useful final answer from your agent

Ask for this compact structure, filled from the real report:

> **Question and comparison:** what was evaluated against what?
> **Evidence:** which candidates were supported, provisional, unresolved, or
> showed no incremental evidence, using the service's actual findings?
> **Next work:** which uncertainty suggests collecting more relevant observations,
> improving a measurement, or testing a revised hypothesis?
> **Limits:** what does this result not establish about future data?
> **Artifacts:** where are the saved report, receipt, and declared contract?

An unresolved feature is not automatically useless. A supported feature is not
automatically ready for production. Keep follow-up experiments separate and
seek approval before using the holdout or spending more credits.
