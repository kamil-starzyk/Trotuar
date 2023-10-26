from square import Square

class Location:
  def __init__(self, name, description, size_x, size_y, size_z, ground_level, squares):
    self.name = name
    self.description = description
    self.size_x = size_x
    self.size_y = size_y
    self.size_z = size_z
    self.ground_level = ground_level
    self.squares = squares

  def to_dict(self):
    return {
      "name": self.name,
      "description": self.description,
      "size_x": self.size_x,
      "size_y": self.size_y,
      "size_z": self.size_z,
      "ground_level": self.ground_level,
      "squares": [member.to_dict() for member in self.members]
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
    squares = [Square.from_dict(square_data) for square_data in squares_list]

    return cls(name, description, size_x, size_y, size_z, ground_level, squares) 