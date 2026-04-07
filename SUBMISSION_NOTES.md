# Production Caveats

1. This solution assumes the bank provides a trustworthy `transaction_id` reference for valid payment settlements; production feeds often require fuzzy matching across amount, date, merchant, and processor references.
2. The rounding logic is intentionally simple and grouped at month level; real systems usually need merchant-level, currency-level, and payout-batch-level aggregation rules.
3. This seed data is clean apart from the planted edge cases, so the matcher would underperform on production issues like partial captures, chargebacks, FX conversion, reversed duplicates, or late file replays.
