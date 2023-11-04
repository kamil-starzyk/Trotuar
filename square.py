from konsola import Konsola
from item import Item

class Square:
  def __init__(self, x, y, z, name, description, exits, items):
    self.x = x
    self.y = y
    self.z = z
    self.location = None
    self.name = name
    self.description = description
    self.exits = {
      "n": exits["n"],
      "e": exits["e"],
      "s": exits["s"],
      "w": exits["w"],
      "u": exits["u"],
      "d": exits["d"]
    }
    self.items = items
    #print(f'{self.name: <16} X: {self.x}, Y: {self.y}, Z: {self.z}')
  
  def show_square(self):
    Konsola.print(self.name, "lyellow")
    Konsola.wrap(self.description, "lwhite")
    Konsola.print("Wyjścia: ", "red", line_end=" ")
    for e in self.exits:
      if self.exits[e]:
        print(e, end=" ")
    print('')
    mobs = []
    for mob in self.location.mobs:
      if mob.x == self.x and mob.y == self.y and mob.z == self.z:
        mobs.append(mob)
    if len(mobs) > 0:
      Konsola.print("Istoty: ", "lgreen")
      for mob in mobs:
        print("  "+mob.name)
    if len(self.items) > 0:
      Konsola.print("Przedmioty: ", "lcyan")
      for i in self.items:
        print("  "+i.name)


  
  def to_dict(self):
    return {
      "x": self.x, 
      "y": self.y,
      "z": self.z,
      "name": self.name,
      "description": self.description,
      "exits": self.exits,
      "items" : [item.to_dict() for item in self.items]
    }
  
  @classmethod
  def from_dict(cls, data):
    items = [Item.from_dict(item_data) for item_data in data["items"]]
    return cls(data["x"], data["y"], data["z"], data["name"], data["description"], data["exits"], items)