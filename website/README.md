# Website workspace

The website agent can put public website source and assets in this folder.
No website implementation or hosting configuration is included yet.

Keep changes here and link to shared public examples rather than copying
private service material. Do not change `plugins/mlreferee/`, its MCP endpoint,
the workflow skill, or the catalog as a side effect of website work.

Never commit credentials, form-delivery secrets, private reviewer information,
customer data/reports, production logs, databases, backend source or deployment
configuration. Put actual secrets in the hosting provider's secure settings.
Do not put personal email addresses into public contact details; use the
existing public support form unless the owner explicitly changes that choice.

Keep demo videos on their approved external host. Do not version recordings,
large generated files, dependency trees or build output. Preserve any required
unlisted/noindex settings for the demo page. Git storage and site publication
are separate: adding website source here does not authorize a hosting cutover,
DNS change, new deployment workflow or production release.

Follow the root [contributing guidance](../CONTRIBUTING.md), LICENSE and NOTICE.
Never imply that a preview connector or pending tool is live or approved.
