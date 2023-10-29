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
  
  def find_square(self, target_x, target_y, target_z):
    for square in self.squares:
      #print(f'{square.name: <16} X: {square.x}, Y: {square.y}, Z: {square.z}')
      #print(f'X: {target_x}, Y: {target_y}, Z: {target_z}')
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
      "squares": [square.to_dict() for square in self.squares]
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