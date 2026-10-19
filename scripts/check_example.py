"""Offline structural checks, not Referee preflight or a leakage guarantee."""

import argparse
import csv
from datetime import datetime
import json
import math
from pathlib import Path


def check(csv_path, contract_path):
    contract = json.loads(contract_path.read_text())
    numeric = [contract["outcome"], *contract["baseline"], *contract["candidates"]]
    roles = [contract["observation_time"], contract["label_available_time"], contract["entity"], *numeric]
    if len(roles) != len(set(roles)):
        raise ValueError("Column roles must be distinct")
    last = {}
    count = 0
    with csv_path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if len(reader.fieldnames or []) != len(set(reader.fieldnames or [])):
            raise ValueError("Duplicate column names")
        if not set(roles) <= set(reader.fieldnames or []):
            raise ValueError("Missing declared columns")
        for row in reader:
            count += 1
            if None in row or any(row[column] is None for column in roles):
                raise ValueError("Malformed CSV row")
            time = datetime.fromisoformat(row[contract["observation_time"]])
            label_time = datetime.fromisoformat(row[contract["label_available_time"]])
            if label_time <= time:
                raise ValueError("These examples require labels to arrive after prediction time")
            entity = row[contract["entity"]]
            if not entity or (entity in last and time <= last[entity]):
                raise ValueError("Each entity must have unique chronological rows")
            last[entity] = time
            if not all(math.isfinite(float(row[column])) for column in numeric):
                raise ValueError("Non-finite numeric value")
    if not count:
        raise ValueError("Empty data")
    return {"rows": count, "baseline_features": len(contract["baseline"]),
            "candidate_features": len(contract["candidates"])}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.csv, args.contract), indent=2))
        print("Local checks passed. No network calls. Live schema and preflight still required.")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Local check failed: {error}\n")
