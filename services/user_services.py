from typing import List
from rich.console import Console
from rich.table import Table
import db

from domain.User import User

_console = Console()


def list_users() -> List[User]:
    return [db.query_user(u["username"]) for u in db.users]


def view_users(users: List[User]) -> None:
    table = Table(title="User List")
    table.add_column("Balance", justify="center", style="green", no_wrap=True)
    table.add_column("Username", justify="center", style='yellow', no_wrap=True)
    table.add_column("First Name", justify="center", style='yellow', no_wrap=True)
    table.add_column("Last Name", justify="center", style='yellow', no_wrap=True)
    for user in users:
        if user:
            table.add_row(user.username, user.firstname, user.lastname, f"{user.balance:.2f}")
    _console.print(table)


def render_users() -> None:
    view_users(list_users())


def add_user(username: str | None = None, password: str | None = None,
             firstname: str | None = None, lastname: str | None = None,
             balance: float | None = None) -> None:
    _console.print("\n   Add New User   ", style="yellow")
    if username is None:
        username = _console.input("Username: ")
    # Check for duplicate username
    if db.username_exists(username):
        _console.print(f"Error: Duplicate username '{username}'. Please choose a different username.", style="red")
        return
    if password is None:
        password = _console.input("Password: ")
    if firstname is None:
        firstname = _console.input("First Name: ")
    if lastname is None:
        lastname = _console.input("Last Name: ")
    if balance is None:
        balance_str = _console.input("Balance: ")
        try:
            balance = float(balance_str)
        except ValueError:
            _console.print("Balance must be a number.", style="red")
            return
    db.add_user_record(username=username, password=password, firstname=firstname, lastname=lastname, balance=balance)
    _console.print(f"\nWelcome {username}! User added.", style="green")


def delete_user() -> None:
    _console.print("\n   Delete User   ", style="yellow")
    username = _console.input("Enter username to delete: ")

    # Check if user is admin
    if username.strip().lower() == "admin":
        _console.print("Cannot delete admin account.", style="red")
        return

    # Check for portfolios owned by user
    user_portfolios = [p for p in db.portfolios if p.get("owner") == username]
    if user_portfolios:
        _console.print(f"User '{username}' owns {len(user_portfolios)} portfolio(s).", style="red")
        remove_choice = _console.input("Would you like to remove all portfolios for this user? (Y/N): ").strip().lower()
        if remove_choice == "y":
            for p in user_portfolios:
                db.portfolios.remove(p)
            _console.print(f"All portfolios for '{username}' have been removed.", style="green")
            confirm_delete = _console.input(f"Would you like to delete user '{username}' now? (Y/N): ").strip().lower()
            if confirm_delete != "y":
                _console.print("User deletion cancelled.", style="yellow")
                return
        else:
            _console.print("User deletion cancelled. Please remove portfolios first if you wish to proceed.", style="yellow")
            return

    # Proceed to delete user
    idx = next((i for i, u in enumerate(db.users) if u.get("username") == username), None)
    if idx is None:
        _console.print("Cannot delete this user (either not found).", style="red")
        return
    del db.users[idx]
    _console.print(f"User '{username}' deleted.", style="green")


__all__ = [
    "list_users",
    "view_users",
    "render_users",
    "add_user",
    "delete_user",
]
