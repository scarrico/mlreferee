# ML Referee for Claude — preview

![ML Referee](assets/logo.png)

This plugin combines a workflow skill with a remote MCP connection to ML Referee,
an independent hosted feature-evaluation service for supervised machine learning
and forecasting. It helps agents prepare evidence, check access, quote costs,
submit explicitly authorized evaluations and interpret results within their limits.

**Preview only:** the configuration targets `https://api.mlreferee.com` for
Claude. Transport activation, client-specific OAuth setup and a real Claude
sign-in test remain prerequisites. This source package has not been approved
or published in Anthropic's directory. Installation is not proof of connectivity.

For Claude Code, after those prerequisites are complete:

```text
/plugin marketplace add scarrico/mlreferee
/plugin install mlreferee@mlreferee
```

Connect with your ML Referee account through the host's secure OAuth interface.
Never put account passwords, application secrets or access tokens into chat.
Sign-in, beta approval and available credits are separate checks. Start with:

> Check my ML Referee access and credits. Do not upload data or submit an evaluation.

Before evaluation, declare the outcome, baseline, complete candidate family,
observation times, label-availability times and validation plan. The agent must
show the quote and obtain authorization before spending credits. Recover retries
by their identifiers rather than creating another evaluation.

During beta use only synthetic, non-personal or genuinely anonymized evaluation
data. Regulated datasets and identifiable or pseudonymized person-level records
are prohibited. Authorized data is sent to the hosted service, even if the
language model runs locally. See [privacy](https://mlreferee.com/privacy) and
[acceptable use](https://mlreferee.com/acceptable-use).

Save reports and their verification receipts before expiry. Minimal fingerprints
and necessary metadata remain afterward. A fingerprint match establishes byte
consistency, not correctness or safety. Use only currently exposed tools; this
package does not activate the pending original-file download tool.

ML Referee does not recommend financial positions, certify safety or compliance,
or guarantee future performance or deployment readiness. Bounded repairs need
prospective confirmation. Delete retained inputs or reports only with permission.

The public integration code and instructions are MIT licensed. Branding is
excluded; see LICENSE and NOTICE. The hosted engine is not included.

[Website](https://mlreferee.com) · [Support](https://mlreferee.com/support) ·
[Beta](https://mlreferee.com/beta) · [Terms](https://mlreferee.com/terms)
