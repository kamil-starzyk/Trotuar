from square import Square
from mob import Mob

class Area:
  def __init__(self, name, squares):
    self.name = name
    self.squares = squares

  def is_square_in_area(self, sq):
    sq_coords = {
      "x": sq.x,
      "y": sq.y,
      "z": sq.z
    }
    if sq_coords in self.squares:
      return True
    return False

  def to_dict(self):
    return {
      "name": self.name,
      "squares": self.squares
    }
  
  @classmethod
  def from_dict(cls, data):
    return cls(data["name"], data["squares"])