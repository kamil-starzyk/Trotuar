from square import Square
from mob import Mob

class Location:
  def __init__(self, name, description, size_x, size_y, size_z, ground_level, squares, mobs):
    self.name = name
    self.description = description
    self.size_x = size_x
    self.size_y = size_y
    self.size_z = size_z
    self.ground_level = ground_level
    self.squares = squares
    self.mobs = mobs
  
  def find_square(self, target_x, target_y, target_z):
    for square in self.squares:
      if square.x == target_x and square.y == target_y and square.z == target_z:
        return square
    return None

  def to_dict(self):
    return {
      "name": self.name,
      "description": self.description,
      "size_x": self.size_x,
      "size_y": self.size_y,
      "size_z": self.size_z,
      "ground_level": self.ground_level,
      "squares": [square.to_dict() for square in self.squares],
      "mobs": [mob.to_dict() for mob in self.mobs]
    }
   
  @classmethod
  def from_dict(cls, data):
    name = data["name"]
    description = data["description"]
    size_x = data["size_x"]
    size_y = data["size_y"]
    size_z = data["size_z"]
    ground_level = data["ground_level"]
    squares_list = data["squares"]
    mobs_list = data["mobs"]
    squares = [Square.from_dict(square_data) for square_data in squares_list]
    mobs = [Mob.from_dict(mob_data) for mob_data in mobs_list]
    location = cls(name, description, size_x, size_y, size_z, ground_level, squares, mobs)
    for square in squares:
      square.location = location
    for mob in mobs:
      mob.current_location = location
    return location