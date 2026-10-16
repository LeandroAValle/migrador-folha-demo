import unittest

from payroll_demo.pipeline import build_snapshot, source_rows, transform_row, validate_row


class PipelineTests(unittest.TestCase):
    def test_deterministic_and_reconciled(self):
        first, second = build_snapshot(), build_snapshot()
        self.assertEqual(first, second)
        metrics = first["metrics"]
        self.assertEqual(metrics["extracted"], metrics["completed"] + metrics["errors"])
        self.assertEqual(metrics["extracted"], sum(item["extracted"] for item in first["byEntity"]))

    def test_missing_required_code_is_never_sent(self):
        bad = next(row for row in source_rows() if not row["requiredCode"])
        self.assertIsNotNone(validate_row(bad))
        result = next(item for item in build_snapshot()["control"] if item["sourceKey"] == bad["sourceKey"])
        self.assertEqual("ERRO", result["status"])
        self.assertNotIn("ENVIADO", result["history"])
        self.assertIsNone(result["payload"])

    def test_business_key_survives_transformation(self):
        row = next(row for row in source_rows() if validate_row(row) is None)
        self.assertEqual(row["sourceKey"], transform_row(row)["externalKey"])


if __name__ == "__main__":
    unittest.main()
