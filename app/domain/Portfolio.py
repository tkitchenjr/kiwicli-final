#Define Portfolio class

class Portfolio():
    def __init__(self, id: int, name:str, description:str, holdings:dict):
        self.id = id
        self.name = name
        self.description = description
        self.holdings = holdings


# Define method to view portfolios
# option should print logged in user's list  of porfolios in table format
# output: ID, Name, Description, Holdings Summary
# If no portfolios exit print "No Portfolios Exist"


# define method to create portfolio
# allow currently logge din user to crate a new portfolio
# prompt for name and description

# define method to delete portfolio

# define method to liquidate holdings