from helper import Helper
from konsola import Konsola
from item import Item
import math #ceil damage
import random #for escape

class Mob:
  
  def __init__(self, x, y, z, name, alias, description, lvl, exp, weight, money, race, proficiency, params, stats, equipment, slots, conversations, knowledge):
    self.x = x
    self.y = y
    self.z = z
    self.current_location = None
    self.name = name
    self.alias = alias
    self.description = description
    self.lvl = lvl
    self.exp = exp
    self.weight = weight
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
    if item and 'body_part' in item.attr:
      self.slots[item.attr['body_part']] = item
      self.equipment.remove(item)
      return item
    return 0
  
  def unequip(self, item_name):
    items = [item for item in self.slots.values() if item is not None]
    item = Helper.find_item(items, item_name)
    if item:
      self.slots[item.attr['body_part']] = None
      self.equipment.append(item)
      return item
    return 0

  def try_to_draw_weapon(self):
    if self.slots["first_hand"] == None:
      for item in self.equipment:
        if "body_part" in item.attr and item.attr["body_part"] == "first_hand":
          self.equip(item.alias[0])
          Konsola.print(self.name + " dobywa " + item.name, "red")
          Helper.sleep(0.5)

    if self.slots["second_hand"] == None:
      for item in self.equipment:
        if "body_part" in item.attr and item.attr["body_part"] == "second_hand":
          self.equip(item.alias[0])
          Konsola.print(self.name + " dobywa " + item.name, "red")
          Helper.sleep(0.5)

  def try_to_escape(self, speed_bonus=0):
    chance = Helper.random(0+self.speed, 50+self.speed)
    chance += speed_bonus
    if chance >= 50:
      exits = self.my_square().exits
      e = random.choice(exits)
      self.move_in_direction(e)
      return e
    return 0


  def move_in_direction(self, direction):
    if direction in self.my_square().exits:
      match direction:
        case "n":
          self.y -= 1
        case "e":
          self.x += 1
        case "s":
          self.y += 1
        case "w":
          self.x -= 1
        case "u":
          self.z += 1
        case "d":
          self.z -= 1
      return direction
      self.stamina_max -= 0.2
    return 0


  def show_equipment(self):
    Konsola.print_item_list(self.equipment)
    print("Pieniądze: ", end='')
    Konsola.print(self.money, "yellow")
  
  def outfit(self):
    for i in self.slots:
      print(i, end=": ")
      Konsola.print(self.slots[i].name, "lwhite") if self.slots[i] else print("-")
    
  def show_stats(self, mob_name=""):
    if not mob_name:
      Konsola.print_stats(self)
    else:
      mobs = self.current_location.mobs_on_square(self.my_square())
      mob = Helper.find_item(mobs, mob_name)
      if mob: 
        Konsola.print_stats(mob)
  
  def show_params(self):
    Konsola.print_params(self)

  def my_square(self):
    return self.current_location.find_square(self.x, self.y, self.z)
  
  def hit(self, mob):
    chance = Helper.random()
    chance += self.dexterity + self.attack/2 - (mob.speed + mob.defence/2)
    Konsola.print("Atakuje: " + self.name, "lyellow")
    damage = 0
    if chance >= 50:
      try:
        weapon = self.slots["first_hand"]
        weapon_damage = weapon.attr["damage"]
        damage = self.damage(mob, weapon_damage)
      except AttributeError:
        damage = self.damage(mob)
      except KeyError:
        damage = self.damage(mob)

    return damage

  def damage_multiplier(self):
    min_range = int(30 + 15*(self.dexterity / 50))
    max_range = int(70 - 15*(self.dexterity / 50))
    damage_multiplier = Helper.random(min_range, max_range)
    # print(f'Min range: {min_range}')
    # print(f'Max range: {max_range}')
    # print(f'Multiplier: {damage_multiplier}')
    # print("")
    return damage_multiplier/50
  
  def damage(self, mob, item_damage=5):
    """
    Method calculates damage given during a blow. If item damage is specified then it will calculate result for it
    otherwise damage will be calcualted for bare hands, which have base damage 5
    Returns:
        float: coefficient calculated with quadratic function
    """
    s_attack = self.stat_coefficient(self.stats["attack"])
    s_dexterity = self.stat_coefficient(self.stats["dexterity"])/2
    s_strength = self.stat_coefficient(self.stats["strength"])
    m_defence = self.stat_coefficient(mob.stats["defence"])

    damage = (s_attack + s_dexterity + s_strength)/3
    damage *= item_damage
    damage *= self.damage_multiplier()
    damage -= m_defence
    if damage <= 0:
      return 0
    return math.ceil(damage)
  
  def stat_coefficient(self, stat):
    """
    In some instances direct value of stat isn't neccessary. Instead some value between 0 and 3 
    will represent how much given stat affect result. This coefficient isn't linear, but rises 
    fastest for small values:
    0 -> 0
    10 -> 1.08
    20 -> 1.92
    30 -> 2.52
    50 -> 3 
    Returns:
        float: coefficient calculated with quadratic function
    """
    coefficient = -0.0012*(stat-50)*(stat-50)+3
    return coefficient 

  def die(self):
    for i in self.equipment:
      self.equipment.remove(i)
      self.my_square().items.append(i)
    for k, v in self.slots.items():
      self.my_square().items.append(v)
      self.slots[k] = None
    dead_body = Item("Corpse", ["trup", "ciało", "cialo"], "Ciało "+self.name, self.description, )
  
  def rest(self, how_long):
    try:
      how_long = int(how_long)
      for i in range(how_long):
        self.hp += 2
        self.stamina += 10
        self.stamina_max += 1
      return how_long
    except ValueError:
      return 0

  def stat_minus_items_attr(self, stat):
    stat_value = self.stats.get(stat, 0)
    for _, slot in self.slots.items():
      try:
        if stat in slot.attr:
          stat_value += slot.attr[stat]
      except AttributeError:
        pass
    return max(0, stat_value) 

  # Getter properties
  @property
  def strength(self):
    """
    Strength is very straight-forwart stat. It determines how much damage an blow will do.
    Range of this stat is 0-50
    Returns:
        int: The item-adjusted strength value.
    """
    return self.stat_minus_items_attr("strength")

  @property
  def attack(self):
    """
    Attack defines overall offensive ability of mob. It partially affects chance of dealing a hit and primarily amount of damage done.
    It also increases chance of dealing critical hit
    Range of this stat is 0-50
    Returns:
        int: The item-adjusted attack value.
    """
    return self.stat_minus_items_attr("attack")

  @property
  def defence(self):
    """
    Defence defines overall defensive ability of mob. It partially decreases chance of being hit and primarily decreases amount of damage received.
    Range of this stat is 0-50
    Returns:
        int: The item-adjusted defence value.
    """
    return self.stat_minus_items_attr("defence")

  @property
  def speed(self):
    """
    Speed determines rate of hits. Higher speed means more occasions to hit enemy. It also reduces chance of being hit.
    This stat is the most negatively affected by items in outfit.
    Range of this stat is 0-50
    Returns:
        int: The item-adjusted speed value.
    """
    return self.stat_minus_items_attr("speed")

  @property
  def dexterity(self):
    """
    Dexterity represents one's ability to hand weapon. It primarily affects chance of dealing a hit and to some extent amount of damage done.
    It increases chance of dealing critical hit more than attack.
    It also narrwows down range of randomness of damage done:
     - 0 dexterity: damage_multiplier(33 - 66), 
     - 50 dexterity: damage_multiplier(45 - 55)
    Range of this stat is 0-50
    Returns:
        int: The item-adjusted sexterity value.
    """
    return self.stat_minus_items_attr("dexterity")

  @property
  def hp(self):
    return self.params["hp"]
  
  @hp.setter
  def hp(self, value):
    if value <= 0:
      self.params["hp"] = 0
    elif value >= self.params["hp_max"]:
      self.params["hp"] = self.params["hp_max"]
    else:
      self.params["hp"] = value
      
  @property
  def hp_max(self):
    return self.params["hp_max"]

  @property
  def stamina(self):
    return self.params["stamina"]
  
  @stamina.setter
  def stamina(self, value):
    if value <= 0:
      self.params["stamina"] = 0
    elif value >= self.stamina_max:
      self.params["stamina"] = self.stamina_max
    else:
      self.params["stamina"] = value

  @property
  def stamina_max(self):
    if self.params["stamina_max"] < self.params["stamina_total"]/2:
      return self.params["stamina_max"]
    return int(self.params["stamina_total"]/2)
    
  @stamina_max.setter
  def stamina_max(self, value):
    if value <= 0:
      self.params["stamina_max"] = 0
    elif value >= self.params["stamina_total"]:
      self.params["stamina_max"] = self.params["stamina_total"]
    else:
      self.params["stamina_max"] = value

  @property
  def mana(self):
    return self.params["mana"]
  
  @property
  def mana_max(self):
    return self.params["mana_max"]
  
  @mana.setter
  def mana(self, value):
    if value <= 0:
      self.params["mana"] = 0
    elif value >= self.params["mana_max"]:
      self.params["mana"] = self.params["mana_max"]
    else:
      self.params["mana"] = value

  @property
  def satiation(self):
    return self.params["satiation"]
  
  @satiation.setter
  def satiation(self, value):
    if value <= 0:
      self.params["satiation"] = 0
    elif value >= self.params["satiation_max"]:
      self.params["satiation"] = self.params["satiation_max"]
    else:
      self.params["satiation"] = value
  
  @property
  def satiation_max(self):
    return self.params["satiation_max"]
    
  @property
  def hydration(self):
    return self.params["hydration"]
  
  @hydration.setter
  def hydration(self, value):
    if value <= 0:
      self.params["hydration"] = 0
    elif value >= self.params["hydration_max"]:
      self.params["hydration"] = self.params["hydration_max"]
    else:
      self.params["hydration"] = value
  
  @property
  def hydration_max(self):
    return self.params["hydration_max"]


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
      "exp": self.exp,
      "weight": self.weight,
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

  @classmethod
  def from_dict(cls, data):
    eq = [Item.from_dict(item_data) for item_data in data["equipment"]]
    slots = data["slots"]
    for key in slots:
      if slots[key] == {}:
        slots[key] = None
      else:
        slots[key] = Item.from_dict(slots[key])
    
    try:
      mob = cls(data["x"], data["y"], data["z"], data["name"], data["alias"], data["description"], data["lvl"], data["exp"], data["weight"], data["money"], data["race"], data["proficiency"], data["params"], data["stats"], eq, slots, data["conversations"], data["knowledge"])
      return mob
    except TypeError:
      print("Nie udało się wczytać danych.")
      print("Aktualnie ładowana postać: "+ data["name"])
      exit()