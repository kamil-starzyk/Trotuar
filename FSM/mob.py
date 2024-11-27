import math

class Mob:
  def __init__(self, name, x, y, hp, hp_max, stamina, stamina_max, satiation, satiation_max, money):
    self.name = name
    self.x = x
    self.y = y
    self.hp = hp
    self.hp_max = hp_max
    self.stamina = stamina
    self.stamina_max = stamina_max
    self.satiation = satiation
    self.satiation_max = satiation_max
    self.money = money
    self.eq = []

  def modify_attribute(self, attribute, amount):
    """Modify a specified attribute (e.g., hp, stamina, satiation)."""
    # Ensure the attribute exists and has a corresponding max attribute
    if hasattr(self, attribute) and hasattr(self, f"{attribute}_max"):
      # Get current and max values
      current_value = getattr(self, attribute)
      max_value = getattr(self, f"{attribute}_max")
      
      # Modify and bound the value
      new_value = current_value + amount
      setattr(self, attribute, max(0, min(new_value, max_value)))
    else:
      raise AttributeError(f"{attribute} is not a valid attribute with a max counterpart.")

  def compare_coordinates(self, x, y):
    return self.x == x and self.y == y

  def find_distance(self, x, y):
    len_x = self.x - x
    x2 = math.pow(len_x, 2)
    len_y = self.y - y
    y2 = math.pow(len_y, 2)
    distance = math.sqrt(x2 + y2)
    return distance
  
  def go_to_coordinates(self, x, y):
    distance = self.find_distance(x, y)
    distance = math.ceil(distance)
    for _ in range(distance):
      if self.stamina <= 0:
        return False, "NO_STAMINA"
      self.modify_attribute("stamina", -1)
    self.x = x
    self.y = y
    return True, "SUCCESS"
    