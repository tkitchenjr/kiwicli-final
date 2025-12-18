from __future__ import annotations
from typing import List

from rich.console import Console
from rich.table import Table

from app.domain.Portfolio import Portfolio
from app.domain.User import User

from app.database import get_session

_console = Console()


def list_users() -> List[User]:
    with get_session() as session:
        return session.query(User).all()

def view_users(users: List[User]) -> None:
    table = Table(title="User List")
    table.add_column("username", justify="center", style="green", no_wrap=True)
    table.add_column("firstname", justify="center", style='yellow', no_wrap=True)
    table.add_column("lastname", justify="center", style='yellow', no_wrap=True)
    table.add_column("balance", justify="center", style='yellow', no_wrap=True)
    for user in users:
        if user:
            table.add_row(user.username, user.firstname, user.lastname, f"{user.balance:.2f}")
    _console.print(table)

def render_users() -> None:
    view_users(list_users())

def add_user(username: str = None, password: str = None, firstname: str = None, lastname: str = None, balance: float = None) -> bool:
    with get_session() as session:
        if username is None:
            _console.print("\n   Add New User   ", style="yellow")
            username = _console.input("Username: ")

        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            if password is None:
                _console.print(f"Error: Duplicate username '{username}'. Please choose a different username.", style="red")
            return False
            
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
                return False
        
        try:
            new_user = User(username=username, password=password, firstname=firstname, lastname=lastname, balance=balance)
            session.add(new_user)
            session.commit()
            if password is None or firstname is None or lastname is None:
                _console.print(f"\nWelcome {username}! User added.", style="green")
            return True
        except Exception as e:
            if password is None or firstname is None or lastname is None:
                _console.print(f"Error adding user: {e}", style="red")
            return False

def delete_user(username: str = None) -> bool:
    if username is None:
        _console.print("\n   Delete User   ", style="yellow")
        username = _console.input("Enter username to delete: ")

    if username.strip().lower() == "admin":
        if username is None:
            _console.print("Cannot delete admin account.", style="red")
        return False
    
    with get_session() as session:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            _console.print("Cannot delete this user (not found).", style="red")
            return False
        
        user_portfolios = session.query(Portfolio).filter_by(owner=username).all()
        if user_portfolios:
            _console.print(f"User '{username}' owns {len(user_portfolios)} portfolio(s).", style="red")
            remove_choice = _console.input("Would you like to remove all portfolios for this user? (Y/N): ").strip().lower()
            
            if remove_choice == "y":
                for portfolio in user_portfolios:
                    session.delete(portfolio)
                session.commit()
                _console.print(f"All portfolios for '{username}' have been removed.", style="green")
                
                confirm_delete = _console.input(f"Would you like to delete user '{username}' now? (Y/N): ").strip().lower()
                if confirm_delete != "y":
                    _console.print("User deletion cancelled.", style="yellow")
                    return False
            else:
                _console.print("User deletion cancelled. Please remove portfolios first if you wish to proceed.", style="yellow")
                return False

        session.delete(user)
        session.commit()
        _console.print(f"User '{username}' deleted.", style="green")
        return True
