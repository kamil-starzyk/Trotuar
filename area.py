from square import Square
from mob import Mob

class Area:
  def __init__(self, name, reference_coordinate, squares):
    self.name = name
    self.reference_coordinate = reference_coordinate
    self.squares = squares

  def are_coordinates_in_area(self, x, y, z):
    sq_coords = {
      "x": x,
      "y": y,
      "z": z
    }
    if sq_coords in self.squares:
      return True
    return False

  def to_dict(self):
    return {
      "name": self.name,
      "reference_coordinate": self.reference_coordinate,
      "squares": self.squares
    }
  
  @classmethod
  def from_dict(cls, data):
    return cls(data["name"], data["reference_coordinate"], data["squares"])