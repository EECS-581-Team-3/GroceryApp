from typing import Optional

class Item:
    def __init__(self, name:str, quantity:int, in_stock:Optional[bool] = None):
        self.name = name
        self.quantity = quantity
        self.in_stock = in_stock

    def updateQuantity(self, quantity:int):
        self.quantity = quantity
    
    def zero(self):
        self.quantity = 0
        self.in_stock = False
    
    def restock(self, quantity:int, in_stock:bool):
        self.quantity = quantity
        self.in_stock = True
