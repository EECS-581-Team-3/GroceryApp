from typing import Dict, List, Optional
from item import Item

class Inventory:
    def __init__(self) -> None:
        self.items = {}

    def add_item(self, new_item, quantity: int = 1) -> None:
        if isinstance(new_item, str):
            key = new_item.strip().lower()
            if key in self.items:
                self.items[key].increase(quantity)
            else:
                self.items[key] = Item(new_item, quantity)
            return self.items[key]
        elif isinstance(new_item, Item):
            key = new_item.name.strip().lower()
            if key in self.items:
                self.items[key].increase(new_item.quantity)
            else:
                self.items[key] = new_item
            return self.items[key]
        else:
            raise TypeError(f"new_item must be str or Item, got {type(new_item)}")

    def get_item(self, name: str) -> Optional[Item]:
        return self.items.get(name.strip().lower())

    def remove_item(self, name: str) -> None:
        key = name.strip().lower()
        if key in self.items:
            del self.items[key]

    def all_items(self) -> List[Item]:
        return list(self.items.values())

    def list_out_of_stock(self):
        return [item for item in self.items.values() if not item.in_stock]

    def __repr__(self):
        return f"Inventory({len(self.items)} items)"