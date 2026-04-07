from __future__ import annotations

from copy import deepcopy
from decimal import Decimal


TRANSACTIONS = [
    {
        "transaction_id": "TXN1001",
        "customer_id": "CUST001",
        "amount": Decimal("120.00"),
        "transaction_date": "2024-01-27",
        "currency": "USD",
        "type": "payment",
    },
    {
        "transaction_id": "TXN1002",
        "customer_id": "CUST002",
        "amount": Decimal("85.50"),
        "transaction_date": "2024-01-28",
        "currency": "USD",
        "type": "payment",
    },
    {
        "transaction_id": "TXN1003",
        "customer_id": "CUST003",
        "amount": Decimal("199.99"),
        "transaction_date": "2024-01-31",
        "currency": "USD",
        "type": "payment",
    },
    {
        "transaction_id": "TXN1004",
        "customer_id": "CUST004",
        "amount": Decimal("45.25"),
        "transaction_date": "2024-01-29",
        "currency": "USD",
        "type": "payment",
    },
    {
        "transaction_id": "TXN1005",
        "customer_id": "CUST005",
        "amount": Decimal("0.335"),
        "transaction_date": "2024-01-30",
        "currency": "USD",
        "type": "payment",
    },
    {
        "transaction_id": "TXN1006",
        "customer_id": "CUST006",
        "amount": Decimal("0.335"),
        "transaction_date": "2024-01-30",
        "currency": "USD",
        "type": "payment",
    },
    {
        "transaction_id": "TXN1007",
        "customer_id": "CUST007",
        "amount": Decimal("0.335"),
        "transaction_date": "2024-01-30",
        "currency": "USD",
        "type": "payment",
    },
    {
        "transaction_id": "TXN1008",
        "customer_id": "CUST008",
        "amount": Decimal("75.00"),
        "transaction_date": "2024-01-30",
        "currency": "USD",
        "type": "payment",
    },
]

SETTLEMENTS = [
    {
        "settlement_id": "SET2001",
        "transaction_id": "TXN1001",
        "original_transaction_id": None,
        "amount": Decimal("120.00"),
        "settlement_date": "2024-01-28",
        "currency": "USD",
        "type": "payment",
    },
    {
        "settlement_id": "SET2002",
        "transaction_id": "TXN1002",
        "original_transaction_id": None,
        "amount": Decimal("85.50"),
        "settlement_date": "2024-01-29",
        "currency": "USD",
        "type": "payment",
    },
    {
        "settlement_id": "SET2003",
        "transaction_id": "TXN1003",
        "original_transaction_id": None,
        "amount": Decimal("199.99"),
        "settlement_date": "2024-02-01",
        "currency": "USD",
        "type": "payment",
    },
    {
        "settlement_id": "SET2004",
        "transaction_id": "TXN1004",
        "original_transaction_id": None,
        "amount": Decimal("45.25"),
        "settlement_date": "2024-01-30",
        "currency": "USD",
        "type": "payment",
    },
    {
        "settlement_id": "SET2005",
        "transaction_id": "TXN1005",
        "original_transaction_id": None,
        "amount": Decimal("0.34"),
        "settlement_date": "2024-01-31",
        "currency": "USD",
        "type": "payment",
    },
    {
        "settlement_id": "SET2006",
        "transaction_id": "TXN1006",
        "original_transaction_id": None,
        "amount": Decimal("0.34"),
        "settlement_date": "2024-01-31",
        "currency": "USD",
        "type": "payment",
    },
    {
        "settlement_id": "SET2007",
        "transaction_id": "TXN1007",
        "original_transaction_id": None,
        "amount": Decimal("0.34"),
        "settlement_date": "2024-01-31",
        "currency": "USD",
        "type": "payment",
    },
    {
        "settlement_id": "SET2008",
        "transaction_id": "TXN1008",
        "original_transaction_id": None,
        "amount": Decimal("75.00"),
        "settlement_date": "2024-01-31",
        "currency": "USD",
        "type": "payment",
    },
    {
        "settlement_id": "SET2008_DUP",
        "transaction_id": "TXN1008",
        "original_transaction_id": None,
        "amount": Decimal("75.00"),
        "settlement_date": "2024-01-31",
        "currency": "USD",
        "type": "payment",
    },
    {
        "settlement_id": "SET2009",
        "transaction_id": None,
        "original_transaction_id": "TXN9999",
        "amount": Decimal("-22.00"),
        "settlement_date": "2024-01-31",
        "currency": "USD",
        "type": "refund",
    },
]


def generate_data() -> tuple[list[dict], list[dict]]:
    """Return deterministic month-end test data with planted reconciliation gaps."""

    return deepcopy(TRANSACTIONS), deepcopy(SETTLEMENTS)
