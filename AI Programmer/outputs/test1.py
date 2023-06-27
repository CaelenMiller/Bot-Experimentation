class Item:
    def __init__(self, name):
        self.name = name

    def use(self):
        print('You cannot use this item.')


class Key(Item):
    def use(self):
        print('You unlocked a door.')
        # Add logic to unlock a door


class HealthPotion(Item):
    def use(self):
        print('You regained some health.')
        # Add logic to increase player's health


class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def get_items(self):
        return self.items


inventory = Inventory()

# Example items
key = Key('Key')
potion = HealthPotion('Health Potion')

# Adding items to the inventory
inventory.add_item(key)
inventory.add_item(potion)

# Using an item from the inventory
use_item = input('Which item would you like to use? ')
for item in inventory.get_items():
    if item.name.lower() == use_item.lower():
        item.use()
        break
else:
    print('Item not found in inventory.')