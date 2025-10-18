from rich.console import Console
from rich.table import Table

#define User class
class User:
    def __init__(self, username:str, password:str, firstname:str, lastname:str, balance:float):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.balance = balance

# define function to handle user login
def get_login_inputs() -> tuple[str,str]:
    username = _console.input("Enter username: ")
    password = _console.input("Enter password: ")
    return [username, password]

# define function to login
def login(username: str, password: str) -> bool:
   username, password = get_login_inputs()

# define function to view users in a table

# define function to add new user

# define function to delete user

#how to make user menu only accesible to admin users
# after login check if user is admin
# if admin show user management menu
# else display error and redirect to main menu

