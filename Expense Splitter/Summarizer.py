"""
summarizer.py — Plain-English summary generator
Expense Splitter Project
No external APIs needed — pure Python logic.
"""

from splitter import compute_balances, compute_settlements, get_stats, get_expenses


# ─── Individual balance line ──────────────────────────────────────

def summarize_balance(name, amount):
    """
    Turn a single balance number into a readable sentence.
    e.g. summarize_balance("Alex", 230.0) → "Alex is owed ₹230.00"
    """
    if amount > 0.01:
        return f"{name} is owed ₹{amount:.2f}"
    elif amount < -0.01:
        return f"{name} owes ₹{abs(amount):.2f}"
    else:
        return f"{name} is all settled up"


# ─── Settlement line ──────────────────────────────────────────────

def summarize_settlement(transaction):
    """
    Turn a settlement dict into a readable sentence.
    e.g. { from: "Sam", to: "Alex", amount: 200 }
        → "Sam should pay Alex ₹200.00"
    """
    return (
        f"{transaction['from']} should pay "
        f"{transaction['to']} ₹{transaction['amount']:.2f}"
    )


# ─── Full balance report ──────────────────────────────────────────

def balance_report():
    """
    Generate a full plain-English balance report for all members.
    Returns a list of strings, one per member.
    """
    balances = compute_balances()
    if not balances:
        return ["No members added yet."]
    return [summarize_balance(name, amt) for name, amt in balances.items()]


# ─── Settlement report ────────────────────────────────────────────

def settlement_report():
    """
    Generate a list of plain-English settlement instructions.
    Returns a list of strings. Empty list means everyone is settled.
    """
    transactions = compute_settlements()
    if not transactions:
        return ["Everyone is settled up! No payments needed."]
    return [summarize_settlement(t) for t in transactions]


# ─── Category breakdown ───────────────────────────────────────────

def category_breakdown():
    """
    Summarize total spending per category.
    Returns list of strings like "Food: ₹720.00 (2 expenses)"
    """
    expenses = get_expenses()
    if not expenses:
        return ["No expenses recorded yet."]

    totals = {}
    counts = {}
    for e in expenses:
        cat = e.get("category", "Other")
        totals[cat] = round(totals.get(cat, 0) + e["amount"], 2)
        counts[cat] = counts.get(cat, 0) + 1

    # Sort by total descending
    sorted_cats = sorted(totals.items(), key=lambda x: -x[1])
    return [
        f"{cat}: ₹{total:.2f} ({counts[cat]} expense{'s' if counts[cat] > 1 else ''})"
        for cat, total in sorted_cats
    ]


# ─── Top spender ──────────────────────────────────────────────────

def top_spender():
    """
    Return a sentence about who has spent the most overall.
    """
    expenses = get_expenses()
    if not expenses:
        return "No expenses yet."

    paid = {}
    for e in expenses:
        paid[e["payer"]] = round(paid.get(e["payer"], 0) + e["amount"], 2)

    top = max(paid, key=paid.get)
    return f"{top} has paid the most so far: ₹{paid[top]:.2f}"


# ─── Full summary (all-in-one) ────────────────────────────────────

def full_summary():
    """
    Print a complete human-readable trip summary to the console.
    Useful for end-of-trip review or sharing over WhatsApp.
    """
    stats = get_stats()

    lines = []
    lines.append("=" * 40)
    lines.append("       EXPENSE SUMMARY")
    lines.append("=" * 40)
    lines.append(f"Total spent   : ₹{stats['total']:.2f}")
    lines.append(f"Expenses      : {stats['count']}")
    lines.append(f"Members       : {stats['members']}")
    lines.append(f"Per person    : ₹{stats['per_person']:.2f}")
    lines.append("")

    lines.append("--- Balances ---")
    for line in balance_report():
        lines.append(f"  {line}")
    lines.append("")

    lines.append("--- Category breakdown ---")
    for line in category_breakdown():
        lines.append(f"  {line}")
    lines.append("")

    lines.append("--- Settle up ---")
    for line in settlement_report():
        lines.append(f"  {line}")
    lines.append("=" * 40)

    return "\n".join(lines)


# ─── Quick test ───────────────────────────────────────────────────
if __name__ == "__main__":
    print(full_summary())
