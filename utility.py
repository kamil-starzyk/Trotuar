from konsola import Konsola
from helper import Helper
from item import Item

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
  
  def see_more(self):
    Konsola.print(self.name, "lcyan")
    Konsola.print(self.description, "lwhite")
    if self.attr:
      Konsola.print("Atrybuty:", "lwhite")
      for k, v in self.attr.items():
        Konsola.print(" " + k, line_end=': ')
        Konsola.print(v, "lwhite")

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
  
  def to_dict(self):
    return {
      'type': self.type,
      'alias': self.alias,
      'name': self.name,
      'description': self.description,
      'lock': self.lock,
      'opened': self.opened,
      'attr': self.attr,
      'items': [item.to_dict() for item in self.items],
      'money': self.money,
      'actions': self.actions
    }
  
  @classmethod
  def from_dict(cls, data):
    items = [Item.from_dict(item_data) for item_data in data["items"]]
    return cls(data["type"], data["alias"], data["name"], data["description"], data["lock"], data["opened"], data["attr"], items, data['money'], data["actions"])
  