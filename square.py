class Square:
  def __init__(self, x, y, z, name, description, exits, items):
    self.x = x
    self.y = y
    self.z = z
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
    print(self.name)
    print(self.description)
    print("Wyjścia: ",end=" ")
    for e in self.exits:
      if self.exits[e]:
        print(e, end=" ")
    print()
    
  def to_dict(self):
    return {
      "x": self.x, 
      "y": self.y,
      "z": self.z,
      "name": self.name,
      "description": self.description,
      "exits": self.exits,
      "items" : self.items
    }
  
  @classmethod
  def from_dict(cls, data):
    return cls(data["x"], data["y"], data["z"], data["name"], data["description"], data["exits"], data["items"])