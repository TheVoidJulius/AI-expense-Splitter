from flask import Flask, request, jsonify, render_template
from splitter import calculate_balances, calculate_settlements

app = Flask(__name__)

expenses = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/expenses", methods=["GET"])
def get_expenses():
    return jsonify(expenses), 200

@app.route("/add-expense", methods=["POST"])
def add_expense():
    data = request.get_json()
    payer = data.get("payer")
    amount = data.get("amount")
    participants = data.get("participants")
    if not payer or not amount or not participants:
        return jsonify({"error": "Missing fields"}), 400
    expense = {
        "payer": payer,
        "amount": amount,
        "participants": participants,
        "desc": data.get("desc", "Expense"),
        "category": data.get("category", "")
    }
    expenses.append(expense)
    return jsonify({"message": "Expense added", "expense": expense}), 201

@app.route("/delete-expense/<int:index>", methods=["DELETE"])
def delete_expense(index):
    if index < 0 or index >= len(expenses):
        return jsonify({"error": "Invalid index"}), 404
    removed = expenses.pop(index)
    return jsonify({"message": "Deleted", "expense": removed}), 200

@app.route("/balances", methods=["GET"])
def get_balances():
    balances = calculate_balances(expenses)
    return jsonify(balances), 200

@app.route("/settlements", methods=["GET"])
def get_settlements():
    balances = calculate_balances(expenses)
    settlements = calculate_settlements(balances)
    return jsonify(settlements), 200

if __name__ == "__main__":
    app.run(debug=True)