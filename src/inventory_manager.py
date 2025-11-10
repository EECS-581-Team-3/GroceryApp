from typing import Dict, List, Optional
from inventory import Inventory
from item import Item
from grocery_list_manager import ListManager
from data_persistence import DataPersistence
from analytics_manager import AnalyticsManager

class InventoryManager:
    def __init__(self):
        self.persistence = DataPersistence()
        self.analytics = AnalyticsManager()
        self.inventory = Inventory()
        self.grocery_list_manager = ListManager()

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

    def RemoveItem(self, name: str):
        """Remove item from inventory and grocery list."""
        self.inventory.remove_item(name)
        self.grocery_list_manager.remove_from_list(name)

    def list_inventory(self):
        return self.inventory.all_items()

    def list_out_of_stock(self):
        return self.inventory.list_out_of_stock()

    def generate_grocery_list(self, list_name="this_week"):
        """Rebuild grocery list from out-of-stock items."""
        return self.grocery_list_manager.generate_grocery_list(self.inventory, list_name)

    def get_grocery_list(self, list_name="this_week"):
        return self.grocery_list_manager.get_list(list_name)
    
    def __repr__(self):
        return "InventoryManager(Inventory + GroceryListManager)"

    def all_items(self) -> List[Item]:
        d = self._items_dict()
        return sorted(d.values(), key=lambda it: it.name.lower())