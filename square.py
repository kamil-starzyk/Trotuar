class Square:
  def __init__(self, x, y, z, name, description, exit_n, exit_e, exit_s, exit_w, exit_u, exit_d):
    self.x = x
    self.y = y
    self.z = z
    self.name = name
    self.description = description
    self.exit_n = exit_n
    self.exit_e = exit_e
    self.exit_s = exit_s
    self.exit_w = exit_w
    self.exit_u = exit_u
    self.exit_d = exit_d
  
  def to_dict(self):
    return {
      "x": self.x, 
      "y": self.y,
      "z": self.z,
      "name": self.name,
      "description": self.description,
      "exit_n": self.exit_n,
      "exit_e": self.exit_e,
      "exit_s": self.exit_s,
      "exit_w": self.exit_w,
      "exit_u": self.exit_u,
      "exit_d": self.exit_d
    }
  
  @classmethod
  def from_dict(cls, data):
    return cls(data["x"], data["y"], data["z"], data["name"], data["description"], 
               data["exit_n"], data["exit_e"], data["exit_s"], data["exit_w"], data["exit_u"], data["exit_d"])