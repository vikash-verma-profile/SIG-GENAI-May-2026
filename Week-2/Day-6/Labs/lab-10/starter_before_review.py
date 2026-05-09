"""
Lab 10 — intentionally flawed banking-style demo API for risk review practice.

FAKE DATA ONLY. Do not use real credentials.
Find issues (security, validation, design), document them, then refactor into a safer design.

Run: uvicorn starter_before_review:app --reload
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# LAB_ISSUE: Hardcoded secret-like string (never do this in production).
ADMIN_TOKEN = "demo-admin-token-12345"

app = FastAPI(title="Banking demo — FOR REVIEW ONLY", version="0.0.1")

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "demo_bank.sqlite3"


def _init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL NOT NULL
        )
        """
    )
    conn.execute("DELETE FROM accounts")
    conn.execute(
        "INSERT INTO accounts (name, balance) VALUES (?, ?)",
        ("Checking", 1000.0),
    )
    conn.execute(
        "INSERT INTO accounts (name, balance) VALUES (?, ?)",
        ("Savings", 2500.0),
    )
    conn.commit()
    conn.close()


_init_db()


class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: float


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/accounts")
def list_accounts(admin_token: str) -> list[dict[str, object]]:
    # LAB_ISSUE: Weak auth — shared token in query string can leak via logs/referrers.
    if admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT id, name, balance FROM accounts").fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "balance": r[2]} for r in rows]


@app.post("/transfer")
def transfer(body: TransferRequest) -> dict[str, str]:
    # LAB_ISSUE: No validation that amount is positive or accounts exist.
    # LAB_ISSUE: Race conditions possible — no transaction wrapping both updates.
    conn = sqlite3.connect(DB_PATH)
    # LAB_ISSUE: SQL injection if names were concatenated — here we use parameters,
    # but transfers should still validate accounts and use transactions.
    conn.execute(
        "UPDATE accounts SET balance = balance - ? WHERE name = ?",
        (body.amount, body.from_account),
    )
    conn.execute(
        "UPDATE accounts SET balance = balance + ? WHERE name = ?",
        (body.amount, body.to_account),
    )
    conn.commit()
    conn.close()
    return {"status": "transferred"}
