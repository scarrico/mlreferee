"""Offline tests. Fixtures are synthetic; no uploads or credit use."""

import copy
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import io

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bike = load("bike", "examples/bike-demand/prepare.py")
checker = load("checker", "scripts/check_example.py")


def source_rows(n=1000):
    start = datetime(2020, 1, 1, tzinfo=timezone(timedelta(hours=9)))
    return [{"time": start + timedelta(hours=i), "count": i,
             "temperature": i / 10} for i in range(n)]


class PreparationTests(unittest.TestCase):
    def test_exact_lags_and_label_time(self):
        raw = source_rows()
        row = bike.build_rows(raw)[0]
        self.assertEqual(row["outcome"], 168)
        self.assertEqual(row["demand_lag_24h"], 144)
        self.assertEqual(row["demand_lag_48h"], 120)
        self.assertEqual(row["demand_lag_168h"], 0)
        self.assertEqual(row["temperature_lag_24h"], 14.4)
        self.assertEqual(datetime.fromisoformat(row["label_available_time"]) -
                         datetime.fromisoformat(row["observation_time"]), timedelta(hours=2))

    def test_present_and_future_observations_do_not_change_predictors(self):
        raw = source_rows()
        before = bike.build_rows(raw)[0]
        for row in raw[168:]:
            row["count"] = 999999
            row["temperature"] = -999
        after = bike.build_rows(raw)[0]
        for column in ["demand_lag_24h", *bike.CANDIDATES]:
            self.assertEqual(before[column], after[column], column)

    def test_checksum_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "archive.zip"
            path.write_bytes(b"not the dataset")
            with self.assertRaisesRegex(ValueError, "checksum"):
                bike.read_source(path)

    def test_failed_download_does_not_save_file(self):
        response = io.BytesIO(b"changed source")
        response.geturl = lambda: bike.SOURCE
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.zip"
            with patch.object(bike.urllib.request, "urlopen", return_value=response):
                with self.assertRaisesRegex(ValueError, "checksum"):
                    bike.download(path)
            self.assertFalse(path.exists())

    def test_cached_download_still_verifies_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.zip"
            path.write_bytes(b"bad cached source")
            with patch.object(bike.urllib.request, "urlopen") as request:
                with self.assertRaisesRegex(ValueError, "checksum"):
                    bike.download(path)
                request.assert_not_called()

    def test_prepare_split_hashes_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run"
            with patch.object(bike, "read_source", return_value=source_rows(8760)):
                bike.prepare(Path("unused"), output)
                with self.assertRaises(FileExistsError):
                    bike.prepare(Path("unused"), output)
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["evaluation_rows"], 7920)
            self.assertEqual(manifest["reserved_holdout_rows"], 672)
            self.assertEqual(checker.check(output / "evaluation.csv", output / "contract.json"),
                             {"rows": 7920, "baseline_features": 1, "candidate_features": 6})
            for name, digest in manifest["files"].items():
                self.assertEqual(digest, hashlib.sha256((output / name).read_bytes()).hexdigest())
            with (output / "evaluation.csv").open() as file:
                evaluation = list(csv.DictReader(file))
            with (output / "holdout.csv").open() as file:
                holdout = list(csv.DictReader(file))
            self.assertLess(evaluation[-1]["observation_time"], holdout[0]["observation_time"])
            self.assertEqual(len(evaluation) + len(holdout) + 168, 8760)

    def test_synthetic_fixture(self):
        example = ROOT / "examples/synthetic-regression"
        self.assertEqual(checker.check(example / "example.csv", example / "contract.json"),
                         {"rows": 400, "baseline_features": 1, "candidate_features": 1})

    def test_invalid_data_rejected(self):
        rows = bike.build_rows(source_rows(170))
        cases = []
        bad = copy.deepcopy(rows)
        bad[0]["label_available_time"] = bad[0]["observation_time"]
        cases.append(bad)
        bad = copy.deepcopy(rows)
        bad[1]["observation_time"] = bad[0]["observation_time"]
        cases.append(bad)
        bad = copy.deepcopy(rows)
        bad[0]["outcome"] = "nan"
        cases.append(bad)
        with tempfile.TemporaryDirectory() as directory:
            contract = Path(directory) / "contract.json"
            contract.write_text(json.dumps(bike.make_contract()))
            path = Path(directory) / "data.csv"
            for bad in cases:
                with self.subTest(bad=bad):
                    with path.open("w", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=bike.FIELDS)
                        writer.writeheader()
                        writer.writerows(bad)
                    with self.assertRaises(ValueError):
                        checker.check(path, contract)
            wrong_contract = bike.make_contract()
            wrong_contract["baseline"] = ["outcome"]
            contract.write_text(json.dumps(wrong_contract))
            with self.assertRaisesRegex(ValueError, "distinct"):
                checker.check(path, contract)


if __name__ == "__main__":
    unittest.main()
