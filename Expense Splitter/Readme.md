# 💸 AI Expense Splitter

A web app to split expenses between friends and groups — instantly see who owes whom and how to settle up.

Built with Python, Flask, and vanilla HTML/CSS/JS.

---

## Features

- Add and delete expenses with description, amount, category, and payer
- Split expenses between any group of members
- Automatically calculates each person's balance
- Greedy settlement algorithm — minimizes the number of transactions to settle all debts
- Plain-English summaries of who owes whom
- Clean dark-themed UI with tabs for Expenses, Balances, and Settle Up

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Templating | Jinja2 |
| Data Storage | In-memory (JSON) |
| Testing | Python unittest |

## Project Structure

AI-expense-Splitter/
└── Expense Splitter/
├── app.py              # Flask routes (add, delete, balances, settlements)
├── splitter.py         # Core logic — balance calculation + settlement algorithm
├── summarizer.py       # Plain-English summaries of balances
├── Expenses.json       # JSON schema for expenses and members
├── templates/
│   └── index.html      # Frontend UI
└── README.md

---
## Getting Started

### 1. Prerequisites

- Python 3.x installed
- pip available

### 2. Install dependencies

```bash
pip install flask
```

### 3. Run the app

```bash
cd "Expense Splitter"
python app.py
```

### 4. Open in browser
http://127.0.0.1:5000

---

## How It Works

### Adding an expense

Send a POST request to `/add-expense` with:

```json
{
  "payer": "Alice",
  "amount": 900,
  "participants": ["Alice", "Bob", "Carol"],
  "desc": "Dinner",
  "category": "Food"
}
```

### API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Loads the UI |
| GET | `/expenses` | Returns all expenses |
| POST | `/add-expense` | Adds a new expense |
| DELETE | `/delete-expense/<index>` | Deletes an expense by index |
| GET | `/balances` | Returns net balance per person |
| GET | `/settlements` | Returns minimum transactions to settle up |

---

## Settlement Algorithm

Uses a greedy algorithm to minimize the number of transactions:

1. Calculates net balance for each person (positive = owed money, negative = owes money)
2. Matches the largest debtor with the largest creditor
3. Repeats until all debts are settled

---

## Example

Three friends share expenses:
- Alice pays ₹900 for dinner (split 3 ways)
- Bob pays ₹300 for transport (split 3 ways)

**Balances:**
- Alice: +₹600
- Bob: +₹200
- Carol: -₹400

**Settlement:**
- Carol pays Alice ₹400 ✓

---

## Roadmap

- [ ] Persistent storage with a database
- [ ] User authentication
- [ ] Export settlements as PDF
- [ ] Mobile app

---

## Authors

- Backend — splitter logic, Flask routes, data storage - @TheVoidJulius
- Frontend — HTML template, UI design, integration - @TheVoidCelestia
