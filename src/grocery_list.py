from item import Item

class GroceryList:
    def __init__(self):
        items: Dict = {}

    def add_item(self, new_item: Item):
        if new_item.name in self.items:
            self.items[new_item.name].quantity += new_item.quantity
            return

        self.items[new_item.name] = new_item

    def change_item_quantity(self, name, quantity):
        if name not in self.items:
            return

        self.items[name].quantity += quantity
        
        if self.items[name].quantity = 0:
            self.items.pop(name)
