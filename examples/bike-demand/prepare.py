"""Prepare public aggregate bike-demand data locally. Never calls ML Referee."""

import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import io
import json
import math
from pathlib import Path
import ssl
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SOURCE = "https://archive.ics.uci.edu/static/public/560/seoul%2Bbike%2Bsharing%2Bdemand.zip"
ARCHIVE_SHA256 = "139e9908f0a3544bb222386855c9ce107e96467306bb8e4ce936aab59e7baac4"
CSV_SHA256 = "373339b71a8935d69e9af0abf26a70744632119862eeb3919efb389a7b749c60"
LIMIT = 10 * 1024 * 1024
KST = timezone(timedelta(hours=9))
CANDIDATES = ["demand_lag_48h", "demand_lag_168h", "hour_sin", "hour_cos",
              "weekend", "temperature_lag_24h"]
FIELDS = ["observation_time", "label_available_time", "entity", "outcome",
          "demand_lag_24h", *CANDIDATES]


def verified_bytes(path, expected):
    if path.stat().st_size > LIMIT:
        raise ValueError("Source exceeds the size limit")
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("Source checksum mismatch; stop and review upstream changes")
    return data


def download(path, ca_file=None):
    if path.exists():
        verified_bytes(path, ARCHIVE_SHA256)
        return
    context = ssl.create_default_context(cafile=str(ca_file) if ca_file else None)
    with urllib.request.urlopen(SOURCE, timeout=60, context=context) as response:
        if not response.geturl().startswith("https://archive.ics.uci.edu/"):
            raise ValueError("Unexpected download destination")
        data = response.read(LIMIT + 1)
    if len(data) > LIMIT or hashlib.sha256(data).hexdigest() != ARCHIVE_SHA256:
        raise ValueError("Download size/checksum mismatch; no file saved")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as output:
        output.write(data)


def read_source(path):
    archive = verified_bytes(path, ARCHIVE_SHA256)
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        info = zipped.getinfo("SeoulBikeData.csv")
        if info.file_size > LIMIT:
            raise ValueError("Expanded source exceeds size limit")
        raw = zipped.read(info)  # Read one named member; never extract archive paths.
    if hashlib.sha256(raw).hexdigest() != CSV_SHA256:
        raise ValueError("CSV checksum mismatch")
    rows = list(csv.DictReader(io.StringIO(raw.decode("cp1252"))))
    if len(rows) != 8760:
        raise ValueError("Unexpected source row count")
    parsed = []
    for row in rows:
        hour = int(row["Hour"])
        if not 0 <= hour < 24:
            raise ValueError("Invalid hour")
        time = datetime.strptime(row["Date"], "%d/%m/%Y").replace(hour=hour, tzinfo=KST)
        count = int(row["Rented Bike Count"])
        temperature = float(row["Temperature(°C)"])
        if count < 0 or not math.isfinite(temperature):
            raise ValueError("Invalid count or temperature")
        if parsed and time - parsed[-1]["time"] != timedelta(hours=1):
            raise ValueError("Source must be unique, sorted and hourly; do not silently repair gaps")
        parsed.append({"time": time, "count": count, "temperature": temperature})
    return parsed


def build_rows(source):
    result = []
    for i in range(168, len(source)):
        time = source[i]["time"]
        result.append({
            "observation_time": time.isoformat(),
            "label_available_time": (time + timedelta(hours=2)).isoformat(),
            "entity": "seoul_system", "outcome": source[i]["count"],
            "demand_lag_24h": source[i - 24]["count"],
            "demand_lag_48h": source[i - 48]["count"],
            "demand_lag_168h": source[i - 168]["count"],
            "hour_sin": round(math.sin(2 * math.pi * time.hour / 24), 8),
            "hour_cos": round(math.cos(2 * math.pi * time.hour / 24), 8),
            "weekend": int(time.weekday() >= 5),
            "temperature_lag_24h": source[i - 24]["temperature"],
        })
    return result


def make_contract():
    contract = json.loads((ROOT / "examples/synthetic-regression/contract.json").read_text())
    contract.update(baseline=["demand_lag_24h"], candidates=CANDIDATES,
                    train_window=1440, embargo_seconds=7200)
    return contract


def prepare(archive, destination):
    source = read_source(archive)
    rows = build_rows(source)
    evaluation, holdout = rows[:-672], rows[-672:]
    # Refuse overwrites: preserve the exact family and artifacts of earlier runs.
    destination.mkdir(parents=True, exist_ok=False)
    for name, subset in [("evaluation.csv", evaluation), ("holdout.csv", holdout)]:
        with (destination / name).open("x", newline="", encoding="utf-8") as output:
            writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(subset)
    (destination / "contract.json").write_text(json.dumps(make_contract(), indent=2) + "\n")
    manifest = {
        "source": SOURCE, "doi": "https://doi.org/10.24432/C5F62R",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "attribution": "Seoul Bike Sharing Demand [Dataset]. (2020). UCI Machine Learning Repository.",
        "source_archive_sha256": ARCHIVE_SHA256, "source_csv_sha256": CSV_SHA256,
        "source_rows": len(source), "lag_warmup_rows_removed": 168,
        "evaluation_rows": len(evaluation), "reserved_holdout_rows": len(holdout),
        "candidates": CANDIDATES, "baseline": ["demand_lag_24h"],
        "timing_assumption": "Predict at hour start (UTC+09:00); count and weather available two hours after source hour start. Assumed, not observed ingestion timestamps.",
        "changes": "Derived calendar and lag features; removed first week; reserved final 28 days. Kept non-functioning hours. No same-hour measured weather used.",
        "holdout_rule": "Do not upload holdout.csv in the first evaluation. Sequential hourly validation may use earlier holdout outcomes after their assumed availability; this is not a 28-day batch forecast.",
        "files": {},
    }
    for name in ("evaluation.csv", "holdout.csv", "contract.json"):
        manifest["files"][name] = hashlib.sha256((destination / name).read_bytes()).hexdigest()
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Prepared {len(evaluation)} evaluation rows, {len(holdout)} reserved rows, {len(CANDIDATES)} candidates.")
    print(f"Saved locally: {destination}. No Referee upload, quote or evaluation was performed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["download", "prepare"])
    parser.add_argument("--archive", type=Path, default=ROOT / "data/seoul-bike.zip")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/bike-demand")
    parser.add_argument("--ca-file", type=Path, help="Trusted CA bundle if Python's certificate store is not configured")
    args = parser.parse_args()
    try:
        if args.action == "download":
            download(args.archive, args.ca_file)
            print(f"Verified public source: {args.archive}. No data uploaded.")
        else:
            prepare(args.archive, args.output)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(1, f"Preparation stopped: {error}\n")


if __name__ == "__main__":
    main()
