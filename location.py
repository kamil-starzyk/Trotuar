from square import Square
from area import Area
from mob import Mob

class Location:
  def __init__(self, name, description, size_x, size_y, size_z, ground_level, squares, mobs, secret_passages, areas):
    self.name = name
    self.description = description
    self.size_x = size_x
    self.size_y = size_y
    self.size_z = size_z
    self.ground_level = ground_level
    self.squares = squares
    self.mobs = mobs
    self.secret_passages = secret_passages
    self.areas = areas
  
  def find_square(self, target_x, target_y, target_z):
    for square in self.squares:
      if square.x == target_x and square.y == target_y and square.z == target_z:
        return square
    return None
  
  def mobs_on_square(self, square):
    mob_list = []
    for mob in self.mobs:
      if mob.my_square == square:
        mob_list.append(mob)
    return mob_list

  def to_dict(self):
    return {
      "name": self.name,
      "description": self.description,
      "size_x": self.size_x,
      "size_y": self.size_y,
      "size_z": self.size_z,
      "ground_level": self.ground_level,
      "squares": [square.to_dict() for square in self.squares],
      "mobs": [mob.to_dict() for mob in self.mobs],
      "secret_passages": self.secret_passages,
      "areas": self.areas
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
    passages = data["secret_passages"]
    areas_list = data["areas"]
    areas = [Area.from_dict(area_data) for area_data in areas_list]
    location = cls(name, description, size_x, size_y, size_z, ground_level, squares, mobs, passages, areas)
    for square in squares:
      square.location = location
    for mob in mobs:
      mob.current_location = location
      mob_area = next((area for area in areas if area.name == mob.area), None)
      mob.area = mob_area
    return location