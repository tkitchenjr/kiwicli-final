from rich.console import Console
from rich.table import Table
import db
from domain.Transactions import Transactions
from datetime import datetime

_console = Console()

def update_transaction_record(transaction_id: str, user_id: str, portfolio_id: str,security_id: str, transaction_type: str, qty: int, price: float, timestamp: str):
    new_transaction = Transactions(
        transaction_id=transaction_id,
        user_id=user_id,
        portfolio_id=portfolio_id,
        security_id=security_id,
        transaction_type=transaction_type,
        qty=qty,
        price=price,
        timestamp=datetime.now()
    )

    db.transactions.append(new_transaction)
    _console.print(f"Transaction recorded: {transaction_type} {qty} of {security_id} at ${price:.2f}", style="green")

def format_timestamp(timestamp) -> str:
    if isinstance(timestamp, datetime):
        return timestamp.strftime("%Y-%m-%d %H:%M")
    else:
        return str(timestamp)

def view_transactions():
    transactions_list = [t for t in db.transactions]

    if not transactions_list:
        _console.print("No transactions found.", style="yellow")
        return

    table = Table(title="Transaction History")
    table.add_column("Transaction ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("User ID", justify="center", style="yellow", no_wrap=True)
    table.add_column("Portfolio ID", justify="center", style="green", no_wrap=True)
    table.add_column("Security ID", justify="center", style="blue", no_wrap=True)
    table.add_column("Type", justify="center", style="magenta", no_wrap=True)
    table.add_column("Quantity", justify="center", style="white", no_wrap=True)
    table.add_column("Price", justify="center", style="green", no_wrap=True)
    table.add_column("Timestamp", justify="center", style="dim", no_wrap=True)
    for t in transactions_list:
        table.add_row(
            str(t.transaction_id),
            str(t.user_id),
            str(t.portfolio_id),
            str(t.security_id),
            str(t.transaction_type),
            str(t.qty),
            f"${t.price:.2f}",
            format_timestamp(t.timestamp)
        )

    _console.print(table)

def query_transactions_by_user():
    user_id = _console.input("Enter User ID to query: ").strip().lower()
    if not user_id:
        _console.print("User ID cannot be empty.", style="red")
        return 
    user_transactions = [t for t in db.transactions if t.user_id == user_id]
    if not user_transactions:
        _console.print(f"No transactions found for User ID: {user_id}", style="yellow")
        return
    table = Table(title=f"Transactions for User ID: {user_id}")
    table.add_column("Transaction ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Portfolio ID", justify="center", style="green", no_wrap=True)
    table.add_column("Security ID", justify="center", style="blue", no_wrap=True)
    table.add_column("Type", justify="center", style="magenta", no_wrap=True)
    table.add_column("Quantity", justify="center", style="white", no_wrap=True)
    table.add_column("Price", justify="center", style="green", no_wrap=True)
    table.add_column("Timestamp", justify="center", style="dim", no_wrap=True)
    for t in user_transactions:
        table.add_row(
            str(t.transaction_id),
            str(t.portfolio_id),
            str(t.security_id),
            str(t.transaction_type),
            str(t.qty),
            f"${t.price:.2f}",
            format_timestamp(t.timestamp)
        )
    _console.print(table)

def query_transactions_by_portfolio():
    portfolio_id = _console.input("Enter Portfolio ID to query: ").strip()
    if not portfolio_id:
        _console.print("Portfolio ID cannot be empty.", style="red")
        return 
    portfolio_transactions = [t for t in db.transactions if t.portfolio_id == portfolio_id]
    if not portfolio_transactions:
        _console.print(f"No transactions found for Portfolio ID: {portfolio_id}", style="yellow")
        return
    table = Table(title=f"Transactions for Portfolio ID: {portfolio_id}")
    table.add_column("Transaction ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("User ID", justify="center", style="green", no_wrap=True)
    table.add_column("Security ID", justify="center", style="blue", no_wrap=True)
    table.add_column("Type", justify="center", style="magenta", no_wrap=True)
    table.add_column("Quantity", justify="center", style="white", no_wrap=True)
    table.add_column("Price", justify="center", style="green", no_wrap=True)
    table.add_column("Timestamp", justify="center", style="dim", no_wrap=True)
    for t in portfolio_transactions:
        table.add_row(
            str(t.transaction_id),
            str(t.user_id),
            str(t.security_id),
            str(t.transaction_type),
            str(t.qty),
            f"${t.price:.2f}",
            format_timestamp(t.timestamp)
        )
    _console.print(table)

def query_transactions_by_security():
    security_id = _console.input("Enter Security ID to query: ").strip().upper()
    if not security_id:
        _console.print("Security ID cannot be empty.", style="red")
        return 
    security_transactions = [t for t in db.transactions if t.security_id == security_id]
    if not security_transactions:
        _console.print(f"No transactions found for Security ID: {security_id}", style="yellow")
        return
    table = Table(title=f"Transactions for Security ID: {security_id}")
    table.add_column("Transaction ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("User ID", justify="center", style="green", no_wrap=True)
    table.add_column("Portfolio ID", justify="center", style="blue", no_wrap=True)
    table.add_column("Type", justify="center", style="magenta", no_wrap=True)
    table.add_column("Quantity", justify="center", style="white", no_wrap=True)
    table.add_column("Price", justify="center", style="green", no_wrap=True)
    table.add_column("Timestamp", justify="center", style="dim", no_wrap=True)
    for t in security_transactions:
        table.add_row(
            str(t.transaction_id),
            str(t.user_id),
            str(t.portfolio_id),
            str(t.transaction_type),
            str(t.qty),
            f"${t.price:.2f}",
            format_timestamp(t.timestamp)
        )
    _console.print(table)