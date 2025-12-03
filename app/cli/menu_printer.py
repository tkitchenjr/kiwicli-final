from cli import constants
from rich.console import Console
from typing import Dict, Tuple 
import db
from domain.MenuFunctions import MenuFunctions
from services.user_services import render_users, add_user, delete_user
from services.portfolio_services import view_all_portfolios, delete_portfolio, create_portfolio, partial_liquidate_holdings
from services.security_services import view_all_securities, place_order
from services.transaction_services import view_transactions, query_transactions_by_user, query_transactions_by_portfolio, query_transactions_by_security

_console = Console()

_menu: Dict[int, str] = {
    constants.login_menu: "------\nLogin Menu\n-----\n1. Login\n0. Exit",
    constants.main_menu: "------\nMain Menu\n-----\n1. Manage Users\n2. Manage Portfolios\n3. Marketplace\n4. Transactions\n0. Logout",
    constants.user_menu: "------\nUser Menu\n-----\n1. View Users\n2. Add User\n3. Delete User\n0. Back to Main Menu",
    constants.portfolio_menu: "------\nPortfolio Menu\n-----\n1. View All Portfolios\n2. Create Portfolio\n3. Delete Portfolio\n4. Liquidate Investment\n0. Back to Main Menu",
    constants.marketplace_menu: "------\nMarketplace Menu\n-----\n1. View Securities\n2. Place Order\n0. Back to Main Menu",
    constants.transaction_menu: "------\nTransaction Menu\n-----\n1. View All Transactions \n2. View Transactions by User\n3. View Transactions by Portfolio\n4. View Transactions by Security\n0. Back to Main Menu"
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
    
# define router function to navigate between menus based on user input
# _router: Dict[MenuFunctions:str]
# "0.1": MenuFunctions(executor=login, navigator = lambda: constants.main_menu)

_router: Dict[str, MenuFunctions] ={
    # Login menu (menu_id = 0)
    "0.1": MenuFunctions(executor=login, navigator = lambda: constants.main_menu),
    # Main menu (menu_id = 1)
    "1.1": MenuFunctions(executor=None, navigator = admin_guard),
    "1.2": MenuFunctions(executor=None, navigator = lambda: constants.portfolio_menu),
    "1.3": MenuFunctions(executor=None, navigator = lambda: constants.marketplace_menu),
    "1.4": MenuFunctions(executor=None, navigator = lambda: constants.transaction_menu),
    # User menu (menu_id = 2)
    "2.1": MenuFunctions(executor=render_users, navigator=lambda: constants.user_menu),
    "2.2": MenuFunctions(executor=add_user, navigator=lambda: constants.user_menu),
    "2.3": MenuFunctions(executor=delete_user, navigator=lambda: constants.user_menu),
    # Portfolio menu (menu_id = 3)
    "3.1": MenuFunctions(executor=view_all_portfolios, navigator=lambda: constants.portfolio_menu),
    "3.2": MenuFunctions(executor=create_portfolio, navigator=lambda: constants.portfolio_menu),
    "3.3": MenuFunctions(executor=delete_portfolio, navigator=lambda: constants.portfolio_menu),
    "3.4": MenuFunctions(executor=partial_liquidate_holdings, navigator=lambda: constants.portfolio_menu),
    # Marketplace menu (menu_id = 4)
    "4.1": MenuFunctions(executor=view_all_securities, navigator=lambda: constants.marketplace_menu),
    "4.2": MenuFunctions(executor=place_order, navigator=lambda: constants.marketplace_menu),
    #Transaction menu (menu_id = 5)
    "5.1": MenuFunctions(executor=view_transactions, navigator=lambda: constants.transaction_menu),
    "5.2": MenuFunctions(executor=query_transactions_by_user, navigator=lambda: constants.transaction_menu),
    "5.3": MenuFunctions(executor=query_transactions_by_portfolio, navigator=lambda: constants.transaction_menu),
    "5.4": MenuFunctions(executor=query_transactions_by_security, navigator=lambda: constants.transaction_menu),
    }

# define function to print error messages
def print_error(error: str):
    _console.print(error, style='red')

# define function to print menus
def print_menu(menu_type: int) -> None:
    _console.print(_menu[menu_type])
    user_input = _console.input("Select a menu: ")
    handle_user_input(menu_type, user_input)

