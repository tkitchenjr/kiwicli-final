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

# define function to add new user
def add_user(username:str, password:str, firstname:str, lastname:str, balance:float) -> User:
	print("\n   Add New User   ")
	username = input("Username: ")
	password = input("Password: ")
	firstname = input("First Name: ")
	lastname = input("Last Name: ")
	balance = (input("Balance: "))

	username = {
		"username":username,
		"password":password,
		"firstname":firstname,
		"lastname":lastname,
		"balance":balance
	}
	print ("\n Welcome {username} !")


# define function to delete user
def delete_user(username:str) -> None:
	import db
	user = db.query_user(username)
	if not user:
		raise Exception ("User not found")
	db.user_list.remove(user)

#how to make user menu only accesible to admin users
# logic on menu printer that routes
# after login check if user is admin
# if admin show user management menu
# else display error and redirect to main menu
