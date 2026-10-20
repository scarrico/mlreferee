"""Offline byte-integrity tests; all artifacts are synthetic and temporary."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "hash_report", ROOT / "examples/report-integrity/hash_report.py")
hashing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hashing)


class ReportIntegrityTests(unittest.TestCase):
    def test_exact_utf8_and_changed_newline(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.txt"
            raw = "Synthetic only: café\r\nsecond line".encode("utf-8")
            path.write_bytes(raw)
            result = hashing.hash_report_text(path)
            self.assertEqual(result, {"representation": "report_text",
                "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
            path.write_bytes(raw + b"\n")
            self.assertNotEqual(hashing.hash_report_text(path)["sha256"], result["sha256"])

    def test_invalid_utf8_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.txt"
            path.write_bytes(b"\xff")
            with self.assertRaises(UnicodeDecodeError):
                hashing.hash_report_text(path)

    def test_original_json_and_text_are_distinct(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.json"
            raw = b'{"report":"Synthetic only\\n"}'
            path.write_bytes(raw)
            result = hashing.hash_report(path, include_text=True)
            self.assertEqual(result["sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(result["text_sha256"], hashlib.sha256(b"Synthetic only\n").hexdigest())
            self.assertNotEqual(result["sha256"], result["text_sha256"])


if __name__ == "__main__":
    unittest.main()
