from typing import Dict, List, Optional
from item import Item

class Inventory:
    def __init__(self) -> None:
        self.items = {}

    def add_item(self, new_item: Item, quantity: int = 1) -> None:
        key = new_item.strip().lower()
        if key in self.items:
            self.items[key].increase(quantity)
        else:
            self.items[key] = Item(new_item, quantity)
        return self.items[key]

    def get_item(self, name: str) -> Optional[Item]:
        return self.items.get(name.strip().lower())

    def remove_item(self, name: str) -> None:
        """Remove an item completely."""
        key = name.strip().lower()
        if key in self.items:
            del self.items[key]

    def all_items(self) -> List[Item]:
        return list(self.items.values())

    def list_out_of_stock(self):
        """Return all out-of-stock items."""
        return [item for item in self.items.values() if not item.in_stock]

    def __repr__(self):
        return f"Inventory({len(self.items)} items)"