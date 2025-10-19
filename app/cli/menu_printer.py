from cli import constants
from rich.console import Console
from typing import Dict, Tuple 
from domain.User import view_users
from domain.MenuFunctions import MenuFunctions
import db 
import session



_console = Console()

_menu: Dict[int, str] = {
    constants.login_menu: "------\nLogin Menu\n-----\n1. Login\n0. Exit",
    constants.main_menu: "------\nMain Menu\n-----\n1. Manage Users\n2. Manage Portfolios\n3. Marketplace\n0. Logout",
    constants.user_menu: "------\nUser Menu\n-----\n1. View Users\n2. Add User\n3. Delete User\n0. Back to Main Menu",
    constants.portfolio_menu: "------\nPortfolio Menu\n-----\n1. View Holdings\n2. Create Portfolio\n3. Delete Portfolio\n4. Liquidate Holdings\n0. Back to Main Menu",
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
        session.current_user = user
        _console.print(f"\nWelcome, {user.firstname}!", style="green")
    except Exception as e:
        raise Exception(f"Login failed: {str(e)}")
    
# define router function to navigate between menus based on user input

from domain.User import add_user, delete_user

def admin_guard():
    if session.current_user and session.current_user.username == "admin":
        return constants.user_menu
    else:
        print_error("Access denied: Only admin can manage users.")
        return constants.main_menu

_router: Dict[str, MenuFunctions] = {
    "0.1": MenuFunctions(executor=login, navigator = lambda: constants.main_menu),
    "1.1": MenuFunctions(executor=None, navigator = admin_guard),
    "1.2": MenuFunctions(executor=None, navigator = lambda: constants.portfolio_menu),
    "1.3": MenuFunctions(executor=None, navigator = lambda: constants.marketplace_menu),
    "2.1": MenuFunctions(executor=lambda: view_users([db.query_user(u["username"]) for u in db.users]), navigator=lambda: constants.user_menu),
    "2.2": MenuFunctions(executor=add_user, navigator=lambda: constants.user_menu),
    "2.3": MenuFunctions(executor=delete_user, navigator=lambda: constants.user_menu),
    # Portfolio menu (menu_id = 3)
    "3.1": MenuFunctions(
        executor=lambda: (lambda pid: (__import__("domain.Portfolio", fromlist=["view_holdings"]).view_holdings(pid)))(int(_console.input("Enter Portfolio ID to view: "))),
        navigator=lambda: constants.portfolio_menu,
    ),
    "3.2": MenuFunctions(
        executor=lambda: __import__("domain.Portfolio", fromlist=["create_portfolio"]).create_portfolio(),
        navigator=lambda: constants.portfolio_menu,
    ),
    "3.3": MenuFunctions(
        executor=lambda: (lambda pid: (__import__("domain.Portfolio", fromlist=["delete_portfolio"]).delete_portfolio(pid)))(int(_console.input("Enter Portfolio ID to delete: "))),
        navigator=lambda: constants.portfolio_menu,
    ),
    "3.4": MenuFunctions(
        executor=lambda: (lambda pid: (__import__("domain.Portfolio", fromlist=["liquidate_holdings"]).liquidate_holdings(pid)))(int(_console.input("Enter Portfolio ID to liquidate: "))),
        navigator=lambda: constants.portfolio_menu,
    ),
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