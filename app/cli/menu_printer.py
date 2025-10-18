import sys 
from typing import Dict
from cli import constants
from rich.console import Console
from rich.table import Table


_console = Console()
_menu: Dict[int, str] = {
    constants.login_menu: "\n1. Login\n0. Exit",
    constants.main_menu: "\n1. Manage Users\n2. Manage Portfolios\n3. Marketplace\n0. Logout",
    constants.user_menu: "\n1. View Users\n2. Add User\n3. Delete User\n0. Back to Main Menu",
    constants.portfolio_menu: "\n1. View Holdings\n2. Create Portfolio\n3. Delete Portfolio\n3. Liquidate Holdings\n0. Back to Main Menu",
    constants.marketplace_menu: "\n1. View Securities\n2. Place Order\n0. Back to Main Menu",
}

# define function to print menus
def print_menu(menu_type: int) -> None:
    _console.print(_menu[menu_type])
    handle_input= _console.input("Select a menu: ")
#define function to handle user input
def handle_input (user_input: int) -> None:
        if user_input == 1:
            print("Username >>>: ")
            user_input = _console.input()
            print("Password >>>: ")
            user_input = _console.input()
        elif user_input == 0:
            sys.exit()
        else:
            print("Invalid input. Please try again.")

# define function to get login inputs 
# change this to call the method built from the user class
def get_login_inputs() -> tuple[str,str]:
    username = _console.input("Enter username: ")
    password = _console.input("Enter password: ")
    return [username, password]
