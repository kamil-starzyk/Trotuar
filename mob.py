from helper import Helper
from konsola import Konsola
from item import Item

class Mob:
  
  def __init__(self, x, y, z, name, alias, description, lvl, race, proficiency, params, stats, equipment, slots, conversations):
    self.x = x
    self.y = y
    self.z = z
    self.current_location = None
    self.name = name
    self.alias = alias
    self.description = description
    self.lvl = lvl
    self.race = race
    self.proficiency = proficiency
    self.params = params
    self.stats = stats
    self.equipment = equipment
    self.slots = slots
    self.conversations = conversations
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
    item = Helper.find_item(self.equipment, item_name)
    if 'body_part' in item.attributes:
      self.slots[item.attributes['body_part']] = item
      return item
    else:
      return 0


  def show_equipment(self):
    Konsola.print_item_list(self.equipment)
  
  def outfit(self):
    for i in self.slots:
      print(i, end=": ")
      Konsola.print(self.slots[i].name, "lwhite") if self.slots[i] else print("-")
      
  def my_square(self):
    return self.current_location.find_square(self.x, self.y, self.z)

  def to_dict(self):
    slots_dict = {}
    for key, value in self.slots.items():
      if value is None:
        slots_dict[key] = {}
      else:
        slots_dict[key] = value.to_dict()
    return {
      "x": self.x, 
      "y": self.y,
      "z": self.z,
      "name": self.name,
      "alias": self.alias,
      "description": self.description,
      "lvl": self.lvl,
      "params": self.params,
      "stats": self.stats,
      "equipment": [item.to_dict() for item in self.equipment],
      "slots": slots_dict,
      "conversations": self.conversations
    }

  @classmethod
  def from_dict(cls, data):
    eq = [Item.from_dict(item_data) for item_data in data["equipment"]]
    slots = data["slots"]
    for key in slots:
      if slots[key] == {}:
        slots[key] = None
      else:
        slots[key] = Item.from_dict(slots[key])
    
    return cls(data["x"], data["y"], data["z"], data["name"], data["alias"], data["description"], data["lvl"], data["race"], data["proficiency"], data["params"], data["stats"], eq, slots, data["conversations"])