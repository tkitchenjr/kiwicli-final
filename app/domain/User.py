from rich.console import Console
from rich.table import Table 
from typing import Dict

_console = Console()

#define User class
class User:
	def __init__(self, username:str, password:str, firstname:str, lastname:str, balance:float):
		self.username = username
		self.password = password
		self.firstname = firstname
		self.lastname = lastname
		self.balance = balance


# define function to view users in a table
def view_users(users: list[User]) -> None:
	table = Table(title="User List")
	table.add_column("Balance", justify="center", style="green", no_wrap=True)
	table.add_column("Username", justify="center", style='yellow', no_wrap=True)
	table.add_column("First Name", justify="center", style='yellow', no_wrap=True)
	table.add_column("Last Name", justify="center", style='yellow', no_wrap=True)
	for user in users:
		if user:
			table.add_row(user.username, user.firstname, user.lastname, f"{user.balance:.2f}")
	_console.print(table)


# define function to add user
def add_user(username:str = None, password:str = None, firstname:str = None, lastname:str = None, balance:float = None) -> None:
	import db
	_console.print("\n   Add New User   ", style="yellow")
	if username is None:
		username = _console.input("Username: ")
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
	new_user = {
		"username": username,
		"password": password,
		"firstname": firstname,
		"lastname": lastname,
		"balance": balance
	}
	db.users.append(new_user)
	_console.print(f"\nWelcome {username}! User added.", style="green")


# define function to delete user interactively
def delete_user() -> None:
    import db
    _console.print("\n   Delete User   ", style="yellow")
    username = _console.input("Enter username to delete: ")
    
    if not db.delete_user(username):
        _console.print("Cannot delete this user (either not found or admin).", style="red")
        return
    
    _console.print(f"User '{username}' deleted.", style="green")
