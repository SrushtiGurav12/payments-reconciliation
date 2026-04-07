import unittest

from data_generator import generate_data
from reconciliation import reconcile_month


class ReconciliationTests(unittest.TestCase):
    def setUp(self) -> None:
        transactions, settlements = generate_data()
        self.report = reconcile_month(transactions, settlements, year=2024, month=1)

    def test_next_month_settlement_is_flagged_as_timing_difference(self) -> None:
        ids = {item["transaction_id"] for item in self.report["next_month_settlements"]}
        self.assertEqual(ids, {"TXN1003"})

    def test_duplicate_settlement_is_detected(self) -> None:
        ids = {item["settlement_id"] for item in self.report["duplicate_settlements"]}
        self.assertEqual(ids, {"SET2008_DUP"})

    def test_orphan_refund_is_detected(self) -> None:
        refunds = self.report["orphan_refunds"]
        self.assertEqual(len(refunds), 1)
        self.assertEqual(refunds[0]["original_transaction_id"], "TXN9999")

    def test_rounding_variance_only_appears_in_aggregate(self) -> None:
        rounding_variances = self.report["rounding_only_variances"]
        self.assertEqual(len(rounding_variances), 1)
        self.assertEqual(
            set(rounding_variances[0]["transaction_ids"]),
            {"TXN1005", "TXN1006", "TXN1007"},
        )
        self.assertEqual(rounding_variances[0]["rounded_variance"], "0.01")

    def test_no_transaction_is_marked_missing_in_this_seed_data(self) -> None:
        self.assertEqual(self.report["missing_settlements"], [])


if __name__ == "__main__":
    unittest.main()
