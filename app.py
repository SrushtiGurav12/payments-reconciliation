from __future__ import annotations

import json
from pathlib import Path

from data_generator import generate_data
from reconciliation import reconcile_month


def build_report(year: int = 2024, month: int = 1) -> dict:
    transactions, settlements = generate_data()
    return reconcile_month(transactions, settlements, year=year, month=month)


def main() -> None:
    report = build_report()
    output_path = Path("output") / "reconciliation_report.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"\nSaved report to {output_path}")


if __name__ == "__main__":
    main()
