# grocery_list.py
from typing import Dict
from item import Item

class GroceryList:
    def __init__(self, name: str = "this_week") -> None:
        self.name = name
        self.items: Dict[str, Item] = {}

    def add_item(self, new_item: Item, quantity: int = 1) -> None:
        """Add a new item or increase existing quantity."""
        key = new_item.strip().lower()
        if key in self.items:
            self.items[key].increase(quantity)
        else:
            self.items[key] = Item(new_item, quantity)
        return self.items[key]

    def change_item_quantity(self, name: str, delta: int) -> None:
        if name not in self.items:
            return

        item = self.items[name]
        item.quantity = (item.quantity or 0) + delta

        if item.quantity <= 0:
            self.items.pop(name)

    def remove_item(self, name: str):
        """Remove an item from the list."""
        key = name.strip().lower()
        if key in self.items:
            del self.items[key]

    def clear(self):
        """Remove all items."""
        self.items.clear()

    def list_items(self):
        """Return all items."""
        return list(self.items.values())

    def __repr__(self):
        return f"GroceryList({self.name}, {len(self.items)} items)"