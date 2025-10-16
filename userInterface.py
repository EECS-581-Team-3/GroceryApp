class UserInterface:
    def __init__(self, inventory_manager):
        self.inventory_manager = inventory_manager
        self.inventory = inventory_manager.inventory

    