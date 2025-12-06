from cli import constants
from typing import Dict
from domain.MenuFunctions import MenuFunctions
from services.user_services import render_users, add_user, delete_user
from services.portfolio_services import view_all_portfolios, delete_portfolio, create_portfolio, partial_liquidate_holdings
from services.security_services import view_all_securities, place_order
from services.transaction_services import view_transactions, query_transactions_by_user, query_transactions_by_portfolio, query_transactions_by_security
from services.login_services import login, admin_guard

_menu: Dict[int, str] = {
    constants.login_menu: "------\nLogin Menu\n-----\n1. Login\n0. Exit",
    constants.main_menu: "------\nMain Menu\n-----\n1. Manage Users\n2. Manage Portfolios\n3. Marketplace\n4. Transactions\n0. Logout",
    constants.user_menu: "------\nUser Menu\n-----\n1. View Users\n2. Add User\n3. Delete User\n0. Back to Main Menu",
    constants.portfolio_menu: "------\nPortfolio Menu\n-----\n1. View All Portfolios\n2. Create Portfolio\n3. Delete Portfolio\n4. Liquidate Investment\n0. Back to Main Menu",
    constants.marketplace_menu: "------\nMarketplace Menu\n-----\n1. View Securities\n2. Place Order\n0. Back to Main Menu",
    constants.transaction_menu: "------\nTransaction Menu\n-----\n1. View All Transactions \n2. View Transactions by User\n3. View Transactions by Portfolio\n4. View Transactions by Security\n0. Back to Main Menu"
}
    
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



