#Define Portfolio class

class Portfolio():
    def __init__(self, id: int, name:str, description:str, holdings:dict):
        self.id = id
        self.name = name
        self.description = description
        self.holdings = holdings


# Define methods to add/remove investments from the holdings list