from item import Item

class Inventory:
    def __init__(self):
        self.inventory: Dict[str, Item] = {}

    def addItem(self, new_item: Item):
        self.inventory[Item.name] = new_item

