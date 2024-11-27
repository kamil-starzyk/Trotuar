class Place:
  def __init__(self, name, description, x, y, purpose, price):
    self.name = name
    self.description = description
    self.x = x
    self.y = y
    self.purpose = purpose
    self.price = price
    self.items = []

  def treat(self, mob):
    if not mob.comapre_coordinates(self.x, self.y):
      return False, "FAIL__NOT_HERE"
    if mob.money <= self.price:
      return False, "FAIL__NO_MONEY"  
    mob.money -= self.price
    mob.modify_attribute("hp", 15)
    return True, "SUCCESS"
    

