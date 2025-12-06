import db
from rich.console import Console
from typing import Tuple
from cli.menu_printer import _router, _menu
from cli import constants

_console = Console()

# handle user input function to navigate between menus 
def handle_user_input(menu_id: int, user_input: str):
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

# define function to handle user login
def get_login_inputs() -> Tuple[str,str]:
    username = _console.input("Enter username: ")
    password = _console.input("Enter password: ")
    return username, password

# login function
def login():
    username, password = get_login_inputs()
    try:
        #query db for user and handle exception
        user = db.query_user(username)
        if not user or user.password != password:
            raise Exception("Invalid username or password")
        db.current_user = user
        _console.print(f"\nWelcome, {user.firstname}!", style="green")
    except Exception as e:
        raise Exception(f"Login failed: {str(e)}")
    

def admin_guard():
    if db.current_user and db.current_user.username == "admin":
        return constants.user_menu
    else:
        print_error("Access denied: Only admin can manage users.")
        return constants.main_menu
    
    # define function to print error messages
def print_error(error: str):
    _console.print(error, style='red')

# define function to print menus
def print_menu(menu_type: int) -> None:
    _console.print(_menu[menu_type])
    user_input = _console.input("Select a menu: ")
    handle_user_input(menu_type, user_input)