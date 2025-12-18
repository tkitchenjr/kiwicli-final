from __future__ import annotations
from rich.console import Console
from typing import Tuple
from app.cli import constants

from app.domain.User import User
    
from app.database import get_session

_console = Console()

current_user = None

def handle_user_input(menu_id: int, user_input: str):
    from app.cli.menu_printer import _router
    try:
        # Convert user_input to int for menu navigation
        input_num = int(user_input)
        
        if input_num == 0:
            if menu_id == constants.login_menu:
                _console.print("Exiting application. Goodbye!", style='green')
                exit(0)
            elif menu_id == constants.main_menu:
                print_menu(constants.login_menu)
            else:
                print_menu(constants.main_menu)
                return

        formatted_user_input = f"{str(menu_id)}.{str(input_num)}"
        menu_functions = _router[formatted_user_input]
        
        if menu_functions.executor:
            menu_functions.executor()
            
        if menu_functions.navigator:
            next_menu = menu_functions.navigator()
            print_menu(next_menu)
            
    except ValueError as e:
        print_error("Please enter a valid menu option")
        print_menu(menu_id)
    except Exception as e:
        print_error(f"Error: {str(e)}")
        print_menu(menu_id)

def get_login_inputs() -> Tuple[str,str]:
    username = _console.input("Enter username: ")
    password = _console.input("Enter password: ")
    return username, password

def login(username: str = None, password: str = None) -> bool:
    global current_user
    # If creds not provided, prompt interactively
    if username is None or password is None:
        username, password = get_login_inputs()

    try:
        with get_session() as session:
            user = session.query(User).filter_by(username=username).first()
            if not user or user.password != password:
                current_user = None
                return False
            
            current_user = username  # Store username string as global
            _console.print(f"\nWelcome, {user.firstname}!", style="green")
            return True
    except Exception:
        current_user = None
        return False

def admin_guard():
    if  current_user == "admin":
        return constants.user_menu
    else:
        print_error("Access denied: Only admin can manage users.")
        return constants.main_menu
    
def print_error(error: str):
    _console.print(error, style='red')

def print_menu(menu_type: int) -> None:
    from app.cli.menu_printer import _menu
    _console.print(_menu[menu_type])
    user_input = _console.input("Select a menu: ")
    handle_user_input(menu_type, user_input)
