from typing import Dict, List, Optional
from inventory import Inventory
from item import Item

class InventoryManager:
    def __init__(self, inventory: object):
        self.inventory = inventory

    def _items_dict(self) -> Dict[str, Item]:
        if isinstance(self.inventory, dict):
            return self.inventory
        for attr in ("_items", "items", "inventory"):
            maybe = getattr(self.inventory, attr, None)
            if isinstance(maybe, dict):
                return maybe
        if hasattr(self.inventory, "all_items") and callable(getattr(self.inventory, "all_items")):
            return {it.name: it for it in self.inventory.all_items()}
        raise TypeError("Unsupported inventory type")

    def _get_item(self, name: str) -> Optional[Item]:
        d = self._items_dict()
        return d.get(name)

    def _store_item(self, item: Item) -> None:
        if hasattr(self.inventory, "addItem") and callable(getattr(self.inventory, "addItem")):
            self.inventory.addItem(item)
            return
        if hasattr(self.inventory, "add_item") and callable(getattr(self.inventory, "add_item")):
            self.inventory.add_item(item)
            return
        d = self._items_dict()
        d[item.name] = item

    def listOutOfStock(self) -> List[Item]:
        return [it for it in self.all_items() if not getattr(it, "inStock", getattr(it, "status", True))]

    def addItem(self, name: str, quantity: int, status: bool):
        existing = self._get_item(name)
        if existing:
            existing.quantity = (existing.quantity or 0) + quantity
            if hasattr(existing, "inStock"):
                existing.inStock = status
            else:
                existing.status = status
            return
        item = Item(name, quantity, status)
        self._store_item(item)

    def changeItemStatus(self, name: str, status: bool):
        item = self._get_item(name)
        if not item:
            return
        if hasattr(item, "inStock"):
            item.inStock = status
        else:
            item.status = status

    def changeItemQuantity(self, name: str, quantity: int):
        item = self._get_item(name)
        if not item:
            return
        item.quantity = quantity

    def generateGroceryList(self):
        raise NotImplementedError

    def all_items(self) -> List[Item]:
        d = self._items_dict()
        return sorted(d.values(), key=lambda it: it.name.lower())