# grocery_list.py
from typing import Dict
from item import Item

class GroceryList:
    def __init__(self) -> None:
        self.items: Dict[str, Item] = {}

    def add_item(self, new_item: Item) -> None:
        if new_item.name in self.items:
            existing = self.items[new_item.name]
            existing.quantity = (existing.quantity or 0) + (new_item.quantity or 0)
            return

        self.items[new_item.name] = new_item

    def change_item_quantity(self, name: str, delta: int) -> None:
        if name not in self.items:
            return

        item = self.items[name]
        item.quantity = (item.quantity or 0) + delta

        if item.quantity <= 0:
            self.items.pop(name)