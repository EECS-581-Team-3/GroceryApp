from inventory import Inventory
from item import Item

class InventoryManager:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory
    
        def listOutOfStock(self):
            out_of_stock: list = []
            for item in inventory:
                if not item.status:
                    out_of_stock.append(item)
            return out_of_stock

        def addItem(self, name: str, quantity: int, status: bool):
            if name in self.inventory:
                self.changeItemQuantity(name, quantity)
                return 

            newItem: Item = Item(name, quantity, status)
            inventory.addItem(item)

        def changeItemStatus(self, name:str, status:bool):
            if name not in self.inventory:
                return

            inventory[name].status = status

        def changeItemQuantity(self, name, quantity):
            if name not in self.inventory:
                return

            inventory[name].quantity += quantity

        def generateGroceryList(): 
            pass

