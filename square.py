class Square:
  def __init__(self, x, y, z, name, description, exits):
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
  
  def to_dict(self):
    return {
      "x": self.x, 
      "y": self.y,
      "z": self.z,
      "name": self.name,
      "description": self.description,
      "exits": self.exits
    }
  
  @classmethod
  def from_dict(cls, data):
    return cls(data["x"], data["y"], data["z"], data["name"], data["description"], data["exits"])