# Claude connector and plugin

**Preview:** configuration and instructions are available here, but real Claude
authentication and directory review are not complete. Do not infer service
availability from local package validation.

## Two complementary integrations

A connector supplies the hosted service's tools through MCP and OAuth. A plugin
also bundles the workflow skill: preparation, consent before spending, result
interpretation, and limits. Both use the same hosted service rather than running
the evaluation engine locally.

The plugin source is [plugins/mlreferee](../plugins/mlreferee/README.md). Its
configured Claude server URL is `https://api.mlreferee.com` (origin root). That
transport and its OAuth setup must be activated and tested before a real Claude
connection is claimed. The established `/mcp` endpoint is used by the existing
OpenAI integration; do not change either endpoint by guessing a fallback.

Users should authorize through their client's secure connection interface.
Never paste a password, client secret, access token, or invitation code into a
public issue or conversation. Account sign-in, beta approval and credits are
separate states. Check access before uploading data or requesting an evaluation.

Claude's hosted apps and Claude Code have different OAuth client flows. A
successful connection in one is not proof that every other client works.
Use the [official authentication guidance](https://claude.com/docs/connectors/building/authentication)
for client-specific setup; do not embed credentials in this repository.

## Inspect locally

```sh
git clone https://github.com/scarrico/mlreferee.git
cd mlreferee
claude plugin validate .
claude plugin validate plugins/mlreferee
```

After the compatibility and sign-in prerequisites above are complete, the
publisher-managed Claude Code catalog can be registered and installed with:

```text
/plugin marketplace add scarrico/mlreferee
/plugin install mlreferee@mlreferee
```

These are catalog installation commands, not evidence of Anthropic directory
approval or a working hosted connection. They are not an installation flow for
every Claude application.

## Directory source

The intended GitHub source is `scarrico/mlreferee`, plugin path
`plugins/mlreferee`. Submit the remote service as an MCP connector separately,
then pair the entries. Submission, approval and publication are separate steps;
none is performed by adding files to this repository.

See Anthropic's [plugin submission guide](https://claude.com/docs/plugins/submit)
and [marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces).
