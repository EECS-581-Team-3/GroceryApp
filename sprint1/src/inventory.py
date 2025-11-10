from typing import Dict, List, Optional
from item import Item

class Inventory:
    def __init__(self) -> None:
        self._items: Dict[str, Item] = {}
        self.inventory = self._items

    def add_item(self, new_item: Item) -> None:
        self._items[new_item.name] = new_item

    def addItem(self, new_item: Item) -> None:
        self.add_item(new_item)

    def get_item(self, name: str) -> Optional[Item]:
        return self._items.get(name)

    def getItem(self, name: str) -> Optional[Item]:
        return self.get_item(name)

    def remove_item(self, name: str) -> None:
        self._items.pop(name, None)

    def removeItem(self, name: str) -> None:
        self.remove_item(name)

    def all_items(self) -> List[Item]:
        return list(self._items.values())

    def allItems(self) -> List[Item]:
        return self.all_items()

    def contains(self, name: str) -> bool:
        return name in self._items

    def __contains__(self, name: str) -> bool:
        return self.contains(name)

    def values(self):
        return self._items.values()

    def items(self):
        return self._items.items()

    def __iter__(self):
        return iter(self._items)

    def clear(self) -> None:
        self._items.clear()