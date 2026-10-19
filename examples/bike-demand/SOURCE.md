# Source, license and changes

**Citation:** Seoul Bike Sharing Demand [Dataset]. (2020). UCI Machine Learning
Repository. https://doi.org/10.24432/C5F62R.

- [Original dataset and metadata](https://archive.ics.uci.edu/dataset/560/seoul+bike+sharing+demand)
- [Original download](https://archive.ics.uci.edu/static/public/560/seoul%2Bbike%2Bsharing%2Bdemand.zip)
- [Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/)
- Source and license reviewed October 19, 2026.

The repository distributes preparation code, not a copy of the third-party
dataset. Local source and derived data retain the source's applicable license
and attribution requirements. When sharing a derived dataset, include this
notice, the license link, and a description of your further changes. MIT covers
our preparation code, not ownership of the original observations.

The source has 8,760 hourly rows with system-wide rental counts, weather and
calendar fields. Our review of the supplied columns found aggregate observations,
not rider identifiers, individual journeys, or pseudonymized person-level records.
That assessment is specific to this pinned file; it does not approve arbitrary
public bike or mobility datasets for upload.

Pinned SHA-256 values:

```text
ZIP: 139e9908f0a3544bb222386855c9ce107e96467306bb8e4ce936aab59e7baac4
CSV: 373339b71a8935d69e9af0abf26a70744632119862eeb3919efb389a7b749c60
```

Our changes: decode the source CSV, interpret dates as day/month/year, attach
UTC+09:00, derive lagged and calendar columns, declare an assumed two-hour label
delay, remove the first week for lag history, and reserve the final four weeks.
No actual ingestion timestamps are supplied by the source. No claim of endorsement
by UCI, the data contributors, or the City of Seoul is made.
