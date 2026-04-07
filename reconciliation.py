from __future__ import annotations

from collections import defaultdict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP


CENT = Decimal("0.01")


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


def quantize_cents(amount: Decimal) -> Decimal:
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


def to_money_str(amount: Decimal) -> str:
    return f"{quantize_cents(amount):.2f}"


def month_bounds(year: int, month: int) -> tuple[date, date]:
    start = date(year, month, 1)
    if month == 12:
        return start, date(year + 1, 1, 1)
    return start, date(year, month + 1, 1)


def reconcile_month(
    transactions: list[dict],
    settlements: list[dict],
    year: int,
    month: int,
) -> dict:
    start, next_month_start = month_bounds(year, month)

    scoped_transactions = [
        tx for tx in transactions if start <= parse_date(tx["transaction_date"]) < next_month_start
    ]
    settlement_lookup: dict[str, list[dict]] = defaultdict(list)
    orphan_settlements = []
    duplicate_settlements = []

    for settlement in settlements:
        settlement_date = parse_date(settlement["settlement_date"])
        if settlement["type"] == "payment" and settlement["transaction_id"]:
            settlement_lookup[settlement["transaction_id"]].append(settlement)
        elif start <= settlement_date < next_month_start:
            orphan_settlements.append(settlement)

    canonical_settlements = {}
    for transaction_id, entries in settlement_lookup.items():
        ordered_entries = sorted(entries, key=lambda item: (item["settlement_date"], item["settlement_id"]))
        canonical_settlements[transaction_id] = ordered_entries[0]
        duplicate_settlements.extend(ordered_entries[1:])

    matched = []
    next_month_settlements = []
    missing_settlements = []
    exact_amount_differences = []
    rounding_candidates = []

    for transaction in scoped_transactions:
        match = canonical_settlements.get(transaction["transaction_id"])
        if match is None:
            missing_settlements.append(
                {
                    "transaction_id": transaction["transaction_id"],
                    "amount": to_money_str(transaction["amount"]),
                    "transaction_date": transaction["transaction_date"],
                    "reason": "No matching bank settlement found.",
                }
            )
            continue

        tx_date = parse_date(transaction["transaction_date"])
        settlement_date = parse_date(match["settlement_date"])
        settlement_delay_days = (settlement_date - tx_date).days
        record = {
            "transaction_id": transaction["transaction_id"],
            "settlement_id": match["settlement_id"],
            "transaction_amount": to_money_str(transaction["amount"]),
            "settlement_amount": to_money_str(match["amount"]),
            "transaction_date": transaction["transaction_date"],
            "settlement_date": match["settlement_date"],
            "settlement_delay_days": settlement_delay_days,
        }

        if settlement_date >= next_month_start:
            record["reason"] = "Settled after month end but within the expected 1-2 day delay."
            next_month_settlements.append(record)
            continue

        matched.append(record)

        if transaction["amount"] != match["amount"]:
            exact_amount_differences.append(
                {
                    **record,
                    "exact_difference": str(match["amount"] - transaction["amount"]),
                }
            )

        if transaction["amount"] != match["amount"] and quantize_cents(transaction["amount"]) == quantize_cents(
            match["amount"]
        ):
            rounding_candidates.append((transaction, match))

    orphan_refunds = []
    transaction_ids = {tx["transaction_id"] for tx in transactions}
    for settlement in orphan_settlements:
        if settlement["type"] != "refund":
            continue
        original_transaction_id = settlement["original_transaction_id"]
        if original_transaction_id not in transaction_ids:
            orphan_refunds.append(
                {
                    "settlement_id": settlement["settlement_id"],
                    "amount": to_money_str(settlement["amount"]),
                    "settlement_date": settlement["settlement_date"],
                    "original_transaction_id": original_transaction_id,
                    "reason": "Refund references an original transaction that does not exist in platform data.",
                }
            )

    rounding_only_variances = []
    if rounding_candidates:
        platform_total_exact = sum((tx["amount"] for tx, _ in rounding_candidates), start=Decimal("0.00"))
        settlement_total = sum((st["amount"] for _, st in rounding_candidates), start=Decimal("0.00"))
        rounded_platform_total = quantize_cents(platform_total_exact)
        rounded_difference = settlement_total - rounded_platform_total
        if rounded_difference != Decimal("0.00"):
            rounding_only_variances.append(
                {
                    "transaction_ids": [tx["transaction_id"] for tx, _ in rounding_candidates],
                    "platform_total_exact": str(platform_total_exact),
                    "platform_total_rounded": to_money_str(platform_total_exact),
                    "settlement_total": to_money_str(settlement_total),
                    "rounded_variance": to_money_str(rounded_difference),
                    "reason": "Each line item rounds cleanly to cents, but the month total is still off when summed.",
                }
            )

    in_month_transaction_total = sum((tx["amount"] for tx in scoped_transactions), start=Decimal("0.00"))
    in_month_settlement_total = sum(
        (
            settlement["amount"]
            for settlement in settlements
            if start <= parse_date(settlement["settlement_date"]) < next_month_start
        ),
        start=Decimal("0.00"),
    )

    report = {
        "assumptions": [
            "Platform transactions are recorded immediately and may carry more than two decimal places before final bank rounding.",
            "Bank payment settlements reference the originating platform transaction_id when the settlement is valid.",
            "A settlement landing 1-2 days after a transaction can still be valid timing-wise, even if it falls in the next month.",
            "Bank data can contain duplicate entries and refunds that reference missing originals.",
        ],
        "summary": {
            "reporting_month": f"{year:04d}-{month:02d}",
            "transaction_count": len(scoped_transactions),
            "settlement_count": len(settlements),
            "matched_in_month_count": len(matched),
            "next_month_settlement_count": len(next_month_settlements),
            "missing_settlement_count": len(missing_settlements),
            "duplicate_settlement_count": len(duplicate_settlements),
            "orphan_refund_count": len(orphan_refunds),
            "rounding_variance_count": len(rounding_only_variances),
            "transaction_total_exact": str(in_month_transaction_total),
            "transaction_total_rounded": to_money_str(in_month_transaction_total),
            "settlement_total_in_month": to_money_str(in_month_settlement_total),
            "net_difference_in_month": to_money_str(in_month_settlement_total - quantize_cents(in_month_transaction_total)),
        },
        "matched_in_month": matched,
        "next_month_settlements": next_month_settlements,
        "missing_settlements": missing_settlements,
        "duplicate_settlements": [
            {
                "settlement_id": item["settlement_id"],
                "transaction_id": item["transaction_id"],
                "amount": to_money_str(item["amount"]),
                "settlement_date": item["settlement_date"],
                "reason": "Duplicate bank settlement entry for a transaction that already has a canonical settlement.",
            }
            for item in duplicate_settlements
        ],
        "orphan_refunds": orphan_refunds,
        "exact_amount_differences": exact_amount_differences,
        "rounding_only_variances": rounding_only_variances,
    }
    return report
