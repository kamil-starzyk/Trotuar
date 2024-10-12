from konsola import Konsola
from item import Item
from utility import Utility
from equipment import Equipment

class Square:
  def __init__(self, x, y, z, name, description, exits, utilities, items):
    self.x = x
    self.y = y
    self.z = z
    self.location = None
    self.name = name
    self.description = description
    self.exits = exits
    self.utilities = utilities
    self.items = items
  
  def show_square(self):
    Konsola.print(self.name, "lyellow")
    Konsola.wrap(self.description, "lwhite")
    Konsola.print("Wyjścia: ", "lred", line_end=" ")
    for e in self.exits:
      print(e, end=" ")
    print('')
    
    mobs = []
    for mob in self.location.mobs:
      if mob.x == self.x and mob.y == self.y and mob.z == self.z:
        mobs.append(mob)
    if len(mobs) > 0:
      Konsola.print("Istoty: ", "lmagenta")
      for mob in mobs:
        print("  "+mob.name)
        pass

    if len(self.items) > 0:
      Konsola.print("Przedmioty: ", "lcyan")
      for i in self.items:
        print("  "+i.name_and_count)
  
  def to_dict(self):
    return {
      "x": self.x, 
      "y": self.y,
      "z": self.z,
      "name": self.name,
      "description": self.description,
      "exits": self.exits,
      "utilities" : [utility.to_dict() for utility in self.utilities],
      "items" : self.items.to_dict()
    }
  
  @classmethod
  def from_dict(cls, data):
    items = Equipment.from_dict(data["items"])
    utilities = [Utility.from_dict(utility_data) for utility_data in data["utilities"]]
    square = cls(data["x"], data["y"], data["z"], data["name"], data["description"], data["exits"], utilities, items)
    for u in square.utilities:
      u.put_on_square(square)
    return square