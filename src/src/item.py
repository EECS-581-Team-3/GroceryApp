from typing import Optional

class Item:
    def __init__(self, name:str, quantity:int, in_stock:Optional[bool] = None):
        self.name = name
        self.quantity = quantity
        self.in_stock = in_stock
        self.location = None

    def updateQuantity(self, quantity:int):
        self.quantity = quantity
    
    def zero(self):
        self.quantity = 0
        self.in_stock = False
    
    def restock(self, quantity:int, in_stock:bool):
        self.quantity = quantity
        self.in_stock = True

    def set_quantity(self, new_quantity: int):
        """Update item quantity and stock status."""
        self.quantity = max(0, new_quantity)
        self.in_stock = self.quantity > 0

    def increase(self, amount: int = 1):
        """Increase quantity by given amount."""
        if amount > 0:
            self.quantity += amount
            self.in_stock = True

    def decrease(self, amount: int = 1):
        """Decrease quantity and update stock status."""
        if amount > 0:
            self.quantity = max(0, self.quantity - amount)
            self.in_stock = self.quantity > 0

    def __repr__(self):
        status = "In Stock" if self.in_stock else "Out of Stock"
        return f"{self.name.title()} (Qty: {self.quantity}, {status})"