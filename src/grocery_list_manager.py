from grocery_list import GroceryList
from enum import Enum

class GroceryListType(Enum):
    THIS_WEEK = 1
    NEXT_WEEK = 2

class GroceryListManager:
    def __init__(self):
        self.grocery_lists: Dict[GroceryListType, GroceryList] = {}

    def add_grocery_list(self, new_grocery_list: GroceryList, grocery_list_type: GroceryListType):
        if grocery_list_type in self.grocery_lists:
            return

        self.grocery_lists[grocery_list_type] = new_grocery_list


