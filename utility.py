from konsola import Konsola
from helper import Helper
from item import Item
from equipment import Equipment

# skrzynia, łóżko, palenisko, zarośla, 
class Utility:
  def __init__(self, id, type, alias, name, description, square_description, lock, opened, attr, items, money, actions):
    self.id = id
    self.type = type
    self.alias = alias
    self.name = name
    self.description = description
    self.square_description = square_description
    self.lock = lock
    self.opened = opened
    self.attr = attr
    self.items = items
    self.money = money
    self.actions = actions
  
  def put_on_square(self, square):
    if self not in square.utilities:
      square.utilities.append(self)
    square.description += " " + self.square_description

  def remove_from_square(self, square):
    if self in square.utilities:
      square.utilities.remove(self)
    if " " + self.square_description in square.description:
      square.description = square.description.replace(" " + self.square_description, "", 1)

  def see_more(self):
    Konsola.print(self.name, "lcyan")
    Konsola.print(self.description, "lwhite")
    if self.attr:
      Konsola.print("Atrybuty:", "lwhite")
      for k, v in self.attr.items():
        Konsola.print(" " + k, line_end=': ')
        Konsola.print(v, "lwhite")
    if self.actions:
      Konsola.print("Możliwe działania:", "lwhite")
      for k, v in self.actions.items():
        Konsola.print(" " + k, line_end=': ')
        Konsola.print(v, "lwhite")

  def show_items(self):
    if "search" not in self.actions:
      Konsola.print("Tego się nie da przeszukać!", "red")
      return 0
    Konsola.print_item_list(self.items)
    print("Pieniądze: ", end='')
    Konsola.print(self.money, "yellow")
  
  def sleep(self):
    if "sleep" not in self.actions:
      return 0
    if "comfort" in self.attr:
      return self.attr["comfort"]
    return 30

  def read(self):
    if "read" not in self.actions:
      return 0
    if "text" not in self.attr:
      Konsola.print("Tu nic nie zostało jeszcze napisane", "red")
      return 0
    Konsola.wrap(self.attr["text"])
    if "duration" in self.attr:
      return self.attr["duration"]
    return 1
    
  
  def to_dict(self):
    return {
      "id": self.id,
      'type': self.type,
      'alias': self.alias,
      'name': self.name,
      'description': self.description,
      'square_description': self.square_description,
      'lock': self.lock,
      'opened': self.opened,
      'attr': self.attr,
      'items': self.items.to_dict(),
      'money': self.money,
      'actions': self.actions
    }
  
  @classmethod
  def from_dict(cls, data):
    items = Equipment.from_dict(data["items"])
    print(data["name"])
    return cls(data["id"], data["type"], data["alias"], data["name"], data["description"], data["square_description"], data["lock"], data["opened"], data["attr"], items, data['money'], data["actions"])
  