from helper import Helper
from konsola import Konsola

class Mob:
  def __init__(self, x, y, z, current_location, name, description, race, proficiency, hp, hp_max, mana, mana_max, strength, attack, defence):
    self.x = x
    self.y = y
    self.z = z
    self.current_location = current_location
    self.name = name
    self.description = description
    self.race = race
    self.proficiency = proficiency
    self.hp = hp
    self.hp_max = hp_max
    self.mana = mana
    self.mana_max = mana_max
    self.strength = strength
    self.attack = attack
    self.defence = defence

    self.equipment = []
    self.first_hand = None
    self.second_hand = None
    self.head = None
    self.body = None
    self.finger = None
    self.neck = None
  
  def pick_up(self, item_name):
    item = Helper.find_item(self.my_square().items, item_name)
    if item:
      self.my_square().items.remove(item)
      self.equipment.append(item)
      return item
    return 0
  
  def drop(self, item_name):
    item = Helper.find_item(self.equipment, item_name)
    if item:
      self.equipment.remove(item)
      self.my_square().items.append(item)
      return item
    return 0

  def use(self, item_name):
    pass
  
  def equip(self, item_name):
    pass

  def show_equipment(self):
    Konsola.print_item_list(self.equipment)
      
  def my_square(self):
    return self.current_location.find_square(self.x, self.y, self.z)