from konsola import Konsola
from helper import Helper

# skrzynia, łóżko, palenisko, zarośla, 
class Utility:
  def __init__(self, type, alias, name, description, lock, opened, attr, items, money, actions):
    self.type = type
    self.alias = alias
    self.name = name
    self.description = description
    self.lock = lock
    self.opened = opened
    self.attr = attr
    self.items = items
    self.money = money
    self.actions = actions
  
  def show_items(self):
    if "search" not in self.actions:
      Konsola.print("Tego się nie da przeszukać!", "red")
      return 0
    Konsola.print_item_list(self.items)
    print("Pieniądze: ", end='')
    Konsola.print(self.money, "yellow")
  
  def sleep(self, mob):
    if "sleep" not in self.actions:
      return 0
    if "comfort" in self.attr:
      return self.attr["comfort"]
    return 30