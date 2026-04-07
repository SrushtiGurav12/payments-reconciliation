# Payments Reconciliation Assessment

This repo contains a compact month-end reconciliation solution for the assessment prompt. It generates deterministic test data, identifies the planted gap types, and writes a JSON report to `output/reconciliation_report.json`.

## Assumptions

- The platform records transactions immediately and can retain more than two decimal places before bank rounding.
- The bank usually references the originating `transaction_id` on valid payment settlements.
- Settlement lag of 1-2 days is operationally normal, even when it crosses month end.
- Refund rows can appear in bank data even if the original platform-side transaction is missing.

## Planted gap types in the seed data

- `TXN1003` settles on `2024-02-01`, so January looks short unless timing is handled.
- `TXN1005` to `TXN1007` each round individually, but their aggregate introduces a `0.01` month-end variance.
- `SET2008_DUP` is a duplicate bank settlement entry.
- `SET2009` is a refund with no matching original transaction.

## Run

```powershell
venv\Scripts\python.exe app.py
venv\Scripts\python.exe -m unittest test_reconciliation.py
```

## What the solution reports

- In-month matches
- Valid next-month settlements
- Missing settlements
- Duplicate settlements
- Orphan refunds
- Rounding-only aggregate variance

## Submission notes

- Code: this repo
- Working output: generated at `output/reconciliation_report.json`
- Tests: `test_reconciliation.py`
- Distilled prompt: `DISTILLED_PROMPT.md`
- Production caveats: `SUBMISSION_NOTES.md`

I did not generate a deployed link or demo video inside this environment.
