from cli import constants
from rich.console import Console
from typing import Dict, Tuple 
from domain.MenuFunctions import MenuFunctions
import db 



_console = Console()
_menu: Dict[int, str] = {
    constants.login_menu: "------\nLogin Menu\n-----\n1. Login\n0. Exit",
    constants.main_menu: "------\nMain Menu\n-----\n1. Manage Users\n2. Manage Portfolios\n3. Marketplace\n0. Logout",
    constants.user_menu: "------\nUser Menu\n-----\n1. View Users\n2. Add User\n3. Delete User\n0. Back to Main Menu",
    constants.portfolio_menu: "------\nPortfolio Menu\n-----\n1. View Holdings\n2. Create Portfolio\n3. Delete Portfolio\n3. Liquidate Holdings\n0. Back to Main Menu",
    constants.marketplace_menu: "------\nMarketplace Menu\n-----\n1. View Securities\n2. Place Order\n0. Back to Main Menu",
}
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
        print_error(f"Error executing menu option: {str(e)}")
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
        _console.print(f"\nWelcome, {user.firstname}!", style="green")
    except Exception as e:
        raise Exception(f"Login failed: {str(e)}")
    
# define router function to navigate between menus based on user input
_router: Dict[str, MenuFunctions] = {
     "0.1": MenuFunctions(executor=login, navigator = lambda: constants.main_menu),
     # Main menu options (menu_id = 1)
     "1.1": MenuFunctions(executor=None, navigator = lambda: constants.user_menu),
     "1.2": MenuFunctions(executor=None, navigator = lambda: constants.portfolio_menu),
     "1.3": MenuFunctions(executor=None, navigator = lambda: constants.marketplace_menu),
} 

# define function to print error messages
def print_error(error: str):
    _console.print(error, style='red')



# define function to print menus
def print_menu(menu_type: int) -> None:
    _console.print(_menu[menu_type])
    user_input = _console.input("Select a menu: ")
    handle_user_input(menu_type, user_input)

# define router function to navigate between menus based on user input
# _router: Dict[MenuFunctions:str]
# "0.1": MenuFunctions(executor=login, navigator = lambda: constants.main_menu)



# define function to get login inputs 
# change this to call the method built from the user class
# define exceptions #