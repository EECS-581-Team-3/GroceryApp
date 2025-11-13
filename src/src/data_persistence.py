import json
from pathlib import Path

class DataPersistence:
    """
    Saves and loads inventory and grocery list data.
    """
    def __init__(self, base_dir="data"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)

    def save_inventory(self, inventory, filename="inventory.json"):
        """Serialize inventory to JSON file."""
        path = self.base_dir / filename
        data = {
            name: {"quantity": item.quantity, "in_stock": item.in_stock}
            for name, item in inventory.items.items()
        }
        path.write_text(json.dumps(data, indent=4))
        return path

    def save_grocery_list(self, grocery_list, filename="grocery_list.json"):
        """Serialize grocery list to JSON file."""
        path = self.base_dir / filename
        data = {
            name: {"quantity": item.quantity}
            for name, item in grocery_list.items.items()
        }
        path.write_text(json.dumps(data, indent=4))
        return path

    def load_inventory(self, inventory_class, item_class, filename="inventory.json"):
        """Load inventory data from file."""
        path = self.base_dir / filename
        if not path.exists():
            return inventory_class()
        data = json.loads(path.read_text())
        inventory = inventory_class()
        for name, vals in data.items():
            inventory.add_item(name, vals.get("quantity", 0))
        return inventory

    def load_grocery_list(self, grocery_list_class, item_class, filename="grocery_list.json"):
        """Load grocery list data from file."""
        path = self.base_dir / filename
        if not path.exists():
            return grocery_list_class()
        data = json.loads(path.read_text())
        grocery_list = grocery_list_class()
        for name, vals in data.items():
            grocery_list.add_item(name, vals.get("quantity", 1))
        return grocery_list