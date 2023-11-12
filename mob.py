from helper import Helper
from konsola import Konsola
from item import Item

class Mob:
  
  def __init__(self, x, y, z, name, alias, description, lvl, money, race, proficiency, params, stats, equipment, slots, conversations, knowledge):
    self.x = x
    self.y = y
    self.z = z
    self.current_location = None
    self.name = name
    self.alias = alias
    self.description = description
    self.lvl = lvl
    self.money = money
    self.race = race
    self.proficiency = proficiency
    self.params = params
    self.stats = stats
    self.equipment = equipment
    self.slots = slots
    self.conversations = conversations
    self.knowledge = knowledge

  def see_more(self):
    Konsola.print(self.name, "lcyan")
    Konsola.print(self.description, "lwhite")
    Konsola.print("Wyposarzenie", "lcyan")
    self.outfit()


  def pick_up(self, item_name):
    item = Helper.find_item(self.my_square().items, item_name)
    if item:
      self.my_square().items.remove(item)
      item_in_eq = Helper.is_item_in_list(item, self.equipment)
      if item.stackable() and item_in_eq:
        item_in_eq.amount += item.amount
      else:
        self.equipment.append(item)
      return item
    return 0
  
  def drop(self, item_name):
    item = Helper.find_item(self.equipment, item_name)
    if item:
      if item.stackable() and item.amount > 1:
        print("Jaką ilość chcesz wyrzucić? (max: " + str(item.amount) + ")")
        amount_to_drop = Konsola.int_input(1, item.amount)
        if amount_to_drop == item.amount:
          self.equipment.remove(item)
        else:
          item = Item.unstack(item, amount_to_drop)
      else:
        self.equipment.remove(item)

      item_on_square = Helper.is_item_in_list(item, self.my_square().items)
      if item.stackable() and item_on_square:
        item_on_square.amount += item.amount
      else:
        self.my_square().items.append(item)
      return item
    return 0

  def use(self, item_name):
    pass
  
  def equip(self, item_name):
    item = Helper.find_item(self.equipment, item_name)
    if 'body_part' in item.attr:
      self.slots[item.attr['body_part']] = item
      return item
    else:
      return 0

  def show_equipment(self):
    Konsola.print_item_list(self.equipment)
  
  def outfit(self):
    for i in self.slots:
      print(i, end=": ")
      Konsola.print(self.slots[i].name, "lwhite") if self.slots[i] else print("-")
    
  def show_stats(self):
    Konsola.print_stats(self)
      
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
      "money": self.money,
      "race": self.race,
      "proficiency": self.proficiency,
      "params": self.params,
      "stats": self.stats,
      "equipment": [item.to_dict() for item in self.equipment],
      "slots": slots_dict,
      "conversations": self.conversations,
      "knowledge": self.knowledge
    }

  def stat_minus_items_attr(self, stat):
    stat_value = self.stats.get(stat, 0)
    for _, slot in self.slots.items():
      try:
        if stat in slot.attr:
          stat_value += slot.attr[stat]
      except AttributeError:
        pass
    return max(0, stat_value) 
  
  def hit(self, mob):
    chance = Helper.random()
    chance += self.dexterity + self.attack/2 - (mob.speed + mob.defence/2)
    Konsola.print("Atakuje: " + self.name, "lyellow")
    print("szansa: " + str(round(chance, 2)))
    return chance
  
  # Getter properties
  @property
  def strength(self):
    return self.stat_minus_items_attr("strength")

  @property
  def attack(self):
    return self.stat_minus_items_attr("attack")

  @property
  def defence(self):
    return self.stat_minus_items_attr("defence")

  @property
  def speed(self):
    return self.stat_minus_items_attr("speed")

  @property
  def dexterity(self):
    return self.stat_minus_items_attr("dexterity")


  @classmethod
  def from_dict(cls, data):
    eq = [Item.from_dict(item_data) for item_data in data["equipment"]]
    slots = data["slots"]
    for key in slots:
      if slots[key] == {}:
        slots[key] = None
      else:
        slots[key] = Item.from_dict(slots[key])
    
    return cls(data["x"], data["y"], data["z"], data["name"], data["alias"], data["description"], data["lvl"], data["money"], data["race"], data["proficiency"], data["params"], data["stats"], eq, slots, data["conversations"], data["knowledge"])