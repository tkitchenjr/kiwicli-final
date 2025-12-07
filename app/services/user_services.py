from typing import List

from rich.console import Console
from rich.table import Table

from domain.Portfolio import Portfolio
from domain.User import User

from database import SessionLocal

_console = Console()


def list_users() -> List[User]:
    with SessionLocal() as session:
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

def add_user() -> None:
    with SessionLocal() as session:
        _console.print("\n   Add New User   ", style="yellow")
        new_username = _console.input("Username: ")

        # Check for duplicate username
        existing_user = session.query(User).filter_by(username=new_username).first()
        existing_user = session.query(User).filter_by(username=new_username).first()
        if existing_user:
            _console.print(f"Error: Duplicate username '{new_username}'. Please choose a different username.", style="red")
            return
        # gather user input
        password = _console.input("Password: ")
        firstname = _console.input("First Name: ")
        lastname = _console.input("Last Name: ")
        balance_str = _console.input("Balance: ")
        
        try:
            balance = float(balance_str)
        except ValueError:
            _console.print("Balance must be a number.", style="red")
            return
        
        #add user to database
        try:
                new_user = User(username=new_username, password=password, firstname=firstname, lastname=lastname, balance=balance)
                session.add(new_user)
                session.commit()
                _console.print(f"\nWelcome {new_username}! User added.", style="green")
        except Exception as e:
            _console.print(f"Error adding user: {e}", style="red")

def delete_user() -> None:
    _console.print("\n   Delete User   ", style="yellow")
    username = _console.input("Enter username to delete: ")

    # Check if user is admin
    if username.strip().lower() == "admin":
        _console.print("Cannot delete admin account.", style="red")
        return
    
    with SessionLocal() as session:
        # Check if user exists
        user = session.query(User).filter_by(username=username).first()
        if not user:
            _console.print("Cannot delete this user (not found).", style="red")
            return
        
        # Check for portfolios owned by user
        user_portfolios = session.query(Portfolio).filter_by(owner=username).all()
        if user_portfolios:
            _console.print(f"User '{username}' owns {len(user_portfolios)} portfolio(s).", style="red")
            remove_choice = _console.input("Would you like to remove all portfolios for this user? (Y/N): ").strip().lower()
            
            if remove_choice == "y":
                # Delete all portfolios for this user
                for portfolio in user_portfolios:
                    session.delete(portfolio)
                session.commit()
                _console.print(f"All portfolios for '{username}' have been removed.", style="green")
                
                confirm_delete = _console.input(f"Would you like to delete user '{username}' now? (Y/N): ").strip().lower()
                if confirm_delete != "y":
                    _console.print("User deletion cancelled.", style="yellow")
                    return
        else:
            _console.print("User deletion cancelled. Please remove portfolios first if you wish to proceed.", style="yellow")
            return

        # Proceed to delete user
        session.delete(user)
        session.commit()
        _console.print(f"User '{username}' deleted.", style="green")
