"""
splitter.py — Core expense split & balance logic
Expense Splitter Project
"""

# ─── Data structure ───────────────────────────────────────────────
#
# expense = {
#   "id":     int       (timestamp)
#   "desc":   str       (e.g. "Dinner at Momo's")
#   "amount": float     (e.g. 600.0)
#   "payer":  str       (e.g. "Alex")
#   "split":  list[str] (e.g. ["Alex", "Sam", "Jordan"])
#   "category": str     (e.g. "Food")
# }
#
# balances = { "Alex": 200.0, "Sam": -100.0, "Jordan": -100.0 }
#   positive = person is owed money
#   negative = person owes money
#
# ──────────────────────────────────────────────────────────────────

import json
import time
import os

DATA_FILE = "expenses.json"


# ─── File helpers ─────────────────────────────────────────────────

def load_data():
    """Load expenses and members from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {"members": [], "expenses": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    """Save expenses and members to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ─── Member management ────────────────────────────────────────────

def add_member(name):
    """Add a new member. Returns True if added, False if already exists."""
    data = load_data()
    name = name.strip()
    if not name:
        raise ValueError("Name cannot be empty.")
    if name in data["members"]:
        return False
    data["members"].append(name)
    save_data(data)
    return True


def remove_member(name):
    """
    Remove a member and all their related expenses.
    Returns True if removed, False if not found.
    """
    data = load_data()
    if name not in data["members"]:
        return False
    data["members"].remove(name)
    data["expenses"] = [
        e for e in data["expenses"]
        if e["payer"] != name and name not in e["split"]
    ]
    save_data(data)
    return True


def get_members():
    """Return the current list of members."""
    return load_data()["members"]


# ─── Expense management ───────────────────────────────────────────

def add_expense(desc, amount, payer, split_with, category="Other"):
    """
    Add a new expense.
    - desc:       short description
    - amount:     total amount paid (float)
    - payer:      name of the person who paid
    - split_with: list of names to split the cost among
    - category:   optional category string
    Raises ValueError for invalid inputs.
    """
    data = load_data()

    desc = desc.strip()
    if not desc:
        raise ValueError("Description cannot be empty.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if payer not in data["members"]:
        raise ValueError(f"Payer '{payer}' is not a member.")
    if not split_with:
        raise ValueError("Must split with at least one person.")
    for name in split_with:
        if name not in data["members"]:
            raise ValueError(f"'{name}' is not a member.")

    expense = {
        "id": int(time.time() * 1000),
        "desc": desc,
        "amount": round(float(amount), 2),
        "payer": payer,
        "split": split_with,
        "category": category,
    }
    data["expenses"].append(expense)
    save_data(data)
    return expense


def delete_expense(expense_id):
    """Delete an expense by ID. Returns True if deleted, False if not found."""
    data = load_data()
    original_len = len(data["expenses"])
    data["expenses"] = [e for e in data["expenses"] if e["id"] != expense_id]
    if len(data["expenses"]) == original_len:
        return False
    save_data(data)
    return True


def get_expenses():
    """Return all expenses."""
    return load_data()["expenses"]


# ─── Balance calculation ──────────────────────────────────────────

def compute_balances():
    """
    Calculate net balance for each member.
    Positive = they are owed money.
    Negative = they owe money.
    Returns dict: { name: balance }
    """
    data = load_data()
    balances = {m: 0.0 for m in data["members"]}

    for expense in data["expenses"]:
        share = round(expense["amount"] / len(expense["split"]), 2)
        # Each person in the split owes their share
        for person in expense["split"]:
            if person in balances:
                balances[person] -= share
        # The payer gets back the full amount
        if expense["payer"] in balances:
            balances[expense["payer"]] += expense["amount"]

    # Round to avoid floating point noise
    return {k: round(v, 2) for k, v in balances.items()}


# ─── Settlement algorithm ─────────────────────────────────────────

def compute_settlements():
    """
    Calculate the minimum transactions needed to settle all debts.
    Uses a greedy algorithm: largest debtor pays largest creditor first.
    Returns list of dicts: [{ "from": str, "to": str, "amount": float }]
    """
    balances = compute_balances()

    # Separate into debtors (owe money) and creditors (are owed money)
    debtors  = sorted(
        [{"name": k, "amount": -v} for k, v in balances.items() if v < -0.01],
        key=lambda x: -x["amount"]
    )
    creditors = sorted(
        [{"name": k, "amount": v}  for k, v in balances.items() if v >  0.01],
        key=lambda x: -x["amount"]
    )

    transactions = []
    i, j = 0, 0

    while i < len(debtors) and j < len(creditors):
        pay = round(min(debtors[i]["amount"], creditors[j]["amount"]), 2)
        transactions.append({
            "from":   debtors[i]["name"],
            "to":     creditors[j]["name"],
            "amount": pay,
        })
        debtors[i]["amount"]  = round(debtors[i]["amount"]  - pay, 2)
        creditors[j]["amount"] = round(creditors[j]["amount"] - pay, 2)

        if debtors[i]["amount"] < 0.01:
            i += 1
        if creditors[j]["amount"] < 0.01:
            j += 1

    return transactions


# ─── Quick summary stats ──────────────────────────────────────────

def get_stats():
    """
    Return summary statistics.
    { "total": float, "count": int, "per_person": float, "members": int }
    """
    data = load_data()
    total = sum(e["amount"] for e in data["expenses"])
    n_members = len(data["members"])
    return {
        "total":      round(total, 2),
        "count":      len(data["expenses"]),
        "per_person": round(total / n_members, 2) if n_members else 0.0,
        "members":    n_members,
    }


# ─── Quick test (run this file directly) ─────────────────────────
if __name__ == "__main__":
    # Reset for testing
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

    add_member("Alex")
    add_member("Sam")
    add_member("Jordan")

    add_expense("Dinner",    600, "Alex",   ["Alex", "Sam", "Jordan"], "Food")
    add_expense("Cab home",  300, "Sam",    ["Sam", "Jordan"],         "Transport")
    add_expense("Ice cream", 120, "Jordan", ["Alex", "Jordan"],        "Food")

    print("Balances:", compute_balances())
    print("Settlements:")
    for t in compute_settlements():
        print(f"  {t['from']} → {t['to']}: ₹{t['amount']}")
    print("Stats:", get_stats())
