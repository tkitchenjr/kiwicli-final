# menu functions execute, navigate, print menus
# menu functions for printing menus, executing methods, and navigating between menus
# use callable because you intend to create functions that can be passed as arguments and invoked later

from typing import Callable

class MenuFunctions:
   def __init__(self, executor: Callable|None = None, navigator: Callable|None = None, printer: Callable| None = None):
        self.executor = executor
        self.navigator = navigator
        self.printer = printer 