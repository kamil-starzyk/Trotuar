from helper import Helper
from konsola import Konsola
from item import Item
from utility import Utility
import math #ceil damage
import random #for escape

class Mob:
  ids = {}
  def __init__(self, mob_id, x, y, z, base_name, name, alias, description, lvl, exp, weight, money, race, proficiency, params, stats, equipment, slots, conversations, knowledge, path, killable, can_duel, is_aggressive, can_ally, affiliation):
    self.mob_id = mob_id
    self.x = x
    self.y = y
    self.z = z
    self.current_location = None
    self.base_name = base_name
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

    self.dest_x = None
    self.dest_y = None
    self.dest_z = None
    self.is_searching_for_route = False
    self.path_to_dest = path
    
    self.chance_bonus = 0
    self.killable = killable
    self.can_duel = can_duel
    self.is_aggressive = is_aggressive
    self.can_ally = can_ally
    self.affiliation = affiliation
    self.direction_history = {
      "n": 0,
      "s": 0,
      "e": 0,
      "w": 0,
      "u": 0,
      "d": 0,
    }
    self.still_count = 1
  

  def see_more(self):
    Konsola.print(self.name, "lcyan")
    Konsola.print(self.description, "lwhite")
    Konsola.print("Wyposarzenie", "lcyan")
    self.outfit()


  def pick_up(self, item_name, player=False):
    item = Helper.find_item(self.my_square.items, item_name, player)
    if item:
      self.my_square.items.remove(item)
      item_in_eq = Helper.is_item_in_list(item, self.equipment)
      if item.stackable() and item_in_eq:
        item_in_eq.amount += item.amount
      else:
        self.equipment.append(item)
      return item
    return 0
  
  def drop(self, item_name, player=False):
    item = Helper.find_item(self.equipment, item_name, player)
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

      item_on_square = Helper.is_item_in_list(item, self.my_square.items)
      if item.stackable() and item_on_square:
        item_on_square.amount += item.amount
      else:
        self.my_square.items.append(item)
      return item
    return 0

  def use(self, item_name, player=False):
    item = Helper.find_item(self.equipment, item_name, player)
    effects = {}
    if item and item.type == "Consumable":
      consumable_attr = ["hp", "stamina", "mana", "satiation", "hydration"]
      for attr_name, attr_value in item.attr.items():
        
        if attr_name in consumable_attr:
          setattr(self, attr_name, getattr(self, attr_name) + attr_value)
          effects[attr_name] = attr_value
        
    return item, effects

  
  def equip(self, item_name, player=False):
    item = Helper.find_item(self.equipment, item_name, player)
    if item and 'body_part' in item.attr:
      self.slots[item.attr['body_part']] = item
      self.equipment.remove(item)
      return item
    return 0
  
  def unequip(self, item_name, player=False):
    items = [item for item in self.slots.values() if item is not None]
    item = Helper.find_item(items, item_name, player)
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
      exits = self.my_square.exits
      e = random.choice(exits)
      self.move_in_direction(e)
      return e
    return 0

  def adjust_stamina(self, s, s_max):
    """
    Method that changes value of stamina and stamina_max with regard to one's endurance
    Returns:
      void
    """
    endurance = self.stat_coefficient(self.stats["endurance"])

    self.stamina += (s / endurance) if s < 0 else (s * endurance)
    self.stamina_max += (s_max / endurance) if s_max < 0 else (s_max * endurance)
    

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
      mobs = self.current_location.mobs_on_square(self.my_square)
      mob = Helper.find_item(mobs, mob_name)
      if mob: 
        Konsola.print_stats(mob)
  
  def show_params(self):
    Konsola.print_params(self)

  
  def hit(self, mob):
    chance = Helper.random()
    chance += self.dexterity + self.attack/2 - (mob.speed + mob.defence/2)
    chance += self.chance_bonus
    if(self.name == "Alwer"):
      print(f'szansa_bonus: {self.chance_bonus}, szansa: {chance}')
  
    Konsola.print(self.name + " atakuje -> " + mob.name, "lyellow")
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
  
  def swing(self, mobs):
    chance = Helper.random()
    chance += self.dexterity + self.attack/2 - (mobs[0].speed + mobs[0].defence/2)
    Konsola.print(self.name + " wykonuje zamach", "lyellow")
    damage_sum = 0
    enemies_hit = []
    if chance >= 60:
      for mob in mobs:
        chance = Helper.random()
        chance += self.attack
        if chance >= 40:
          enemies_hit.append(mob)
      
      for enemy in enemies_hit:
        try:
          weapon = self.slots["first_hand"]
          weapon_damage = weapon.attr["damage"]
          damage = self.damage(mob, weapon_damage)
        except AttributeError:
          damage = self.damage(mob)
        except KeyError:
          damage = self.damage(mob)
        enemy.hp -= damage
        damage_sum += damage
        enemy.adjust_stamina(-damage/2, -damage/4)
    
    return len(enemies_hit), damage_sum



  def add_destination(self, x, y, z):
    if self.current_location.find_square(x, y, z):
      self.dest_x = x
      self.dest_y = y
      self.dest_z = z
      self.is_searching_for_route = True
      return True
    print("There is no square with this coordinates")
    return 0
  
  def move_in_direction(self, direction):
    if direction in self.my_square.exits:
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
      self.adjust_stamina(0.5, -0.2)
    return 0
     
  def is_on_square(self, x, y, z):
    if self.x == x and self.y == y and self.z == z:
      return True
    return False

  def recursive_pathfinder(self, x, y, z, visited):
    if (x, y, z) in visited:
      return 0
    if (x, y, z) == (self.dest_x, self.dest_y, self.dest_z):
      return []

    visited.append((x, y, z))
    square = self.current_location.find_square(x, y, z)
    if square:
      exits = square.exits
      for direction in exits:
        if direction == "n":
          path = self.recursive_pathfinder(x, y-1, z, visited)
          if isinstance(path, list):
            path.append(direction)
            return path
        elif direction == "e":
          path = self.recursive_pathfinder(x+1, y, z, visited)
          if isinstance(path, list):
            path.append(direction)
            return path
        elif direction == "s":
          path = self.recursive_pathfinder(x, y+1, z, visited)
          if isinstance(path, list):
            path.append(direction)
            return path
        elif direction == "w":
          path = self.recursive_pathfinder(x-1, y, z, visited)
          if isinstance(path, list):
            path.append(direction)
            return path
        elif direction == "u":
          path = self.recursive_pathfinder(x, y, z+1, visited)
          if isinstance(path, list):
            path.append(direction)
            return path
        elif direction == "d":
          path = self.recursive_pathfinder(x, y, z-1, visited)
          if isinstance(path, list):
            path.append(direction)
            return path
      return 0

    else:
      return 0


  def find_path_to_coordinates(self, x, y, z):
    self.add_destination(x,y,z)
    visited = []
    paths = []
    path = 1
    while path:
      x = self.x
      y = self.y
      z = self.z
      if (x, y, z) in visited:
        visited.remove((x, y, z)) 
      path = self.recursive_pathfinder(x, y, z, visited)
      if path in paths:
        path = 0
      if isinstance(path, list):
        path.reverse()
        paths.append(path)
    shortest_path = None
    if len(paths) > 0:
      shortest_path = min(paths, key=len)
    self.path_to_dest = shortest_path

  def follow_path(self):
    if self.path_to_dest and len(self.path_to_dest) > 0:
      step = self.path_to_dest.pop()
      self.move_in_direction(step)
      return step
    
    self.is_searching_for_route = False
    return None

  def call_for_help(self):
    allies = self.find_mobs_in_radius(5, affiliation=self.affiliation[0])
    for a in allies:
      a.find_path_to_coordinates(self.z, self.y, self.z)
    return len(allies)
  def calculate_distance(self, x, y, z):
    a = self.x - x
    b = self.y - y
    c = self.z - z
    diagonal_ab = math.sqrt(a**2 + b**2)
    diagonal_ac = math.sqrt(diagonal_ab**2 + c**2)
    return diagonal_ac
  
  def find_mobs_in_radius(self, r, base_name="", affiliation=""):
    mobs = []
    if base_name:
      mobs = [mob for mob in self.current_location.mobs if mob.base_name == base_name]
    elif affiliation:
      mobs = [mob for mob in self.current_location.mobs if affiliation in mob.affiliation]
    
    mobs_in_radius = [mob for mob in mobs if mob.calculate_distance(self.x, self.y, self.z) <= r]
    
    return mobs_in_radius

  def random_walk(self):
    exits = self.my_square.exits
    #im dłużej stoi tym większa szansa, że się ruszy
    is_moving = any(count > 0 for count in self.direction_history.values())

    if self.still_count > 0:
      wants_to_move = random.randint(0,10)
      if wants_to_move + self.still_count > 10:
        self.still_count = 0
        e = random.choice(exits)
        self.direction_history[e] = 10
        # print("    Mob decided to move "+ e)
        self.move_in_direction(e)
        return e
      else:
        self.still_count+=1
        # print("    Mob stays still")
        
    
    

    elif is_moving:
      direction = max(self.direction_history, key=self.direction_history.get)
      wants_to_stop = random.randint(0,10) + self.direction_history[direction]
      wants_to_change_direction = random.randint(0,10) + self.direction_history[direction]
      if direction not in exits:
        wants_to_change_direction = 100 + random.randint(-1,1)
        wants_to_stop = 100
        direction = random.choice(exits)
      
      
      if wants_to_change_direction > wants_to_stop and wants_to_change_direction > 13:
        e = direction
        while e==direction and len(exits) > 1:
          e = random.choice(exits)
        self.direction_history[direction] = 0
        self.direction_history[e] = 1
        # print("    Mob decided to switch direction to "+ e)
        self.move_in_direction(e)
        return e
        
      elif wants_to_stop >= wants_to_change_direction and wants_to_stop > 13:
        self.direction_history[direction] = 0
        self.still_count+=1
        # print("    Mob decided to stop ")
        

      else:
        # print("    Mob keeps moving "+ direction)
        self.direction_history[direction] +=1
        self.move_in_direction(direction)
        return direction
        

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
        int: damage ceiled up
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
    for k, v in self.slots.items():
      if v:
        self.my_square.items.append(v)
        self.slots[k] = None
    aliases = ["trup", "ciało", "cialo", "martwy "+self.name]
    aliases = aliases + self.alias
    dead_body = Utility("Corpse", aliases, "Martwy "+self.name, self.description, 0, 1, {}, self.equipment, 0, {"search": "Przeszukaj"})
    self.my_square.utilities.append(dead_body)
    self.my_square.description += " Leży tu [i]martwy " + self.name +"[/i]. "
    self.x=0
    self.y=0
    self.z=0
  
  def rest(self, how_long):
    try:
      how_long = int(how_long)
      for i in range(how_long):
        self.hp += 4
        self.adjust_stamina(15, 2)
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
        int: The item-adjusted dexterity value.
    """
    return self.stat_minus_items_attr("dexterity")

  @property
  def endurance(self):
    """
    Endurance tells how quickly someone gets tired, and ho fast he regenerates
    Range of this stat is 0-50
    Returns:
        int: The item-adjusted endurance value.
    """
    return self.stat_minus_items_attr("endurance")

  @property
  def hp(self):
    return int(self.params["hp"])
  
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
    return int(self.params["hp_max"])

  @property
  def stamina(self):
    return int(self.params["stamina"])
  
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
      return int(self.params["stamina_max"])
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
    return int(self.params["mana"])
  
  @property
  def mana_max(self):
    return int(self.params["mana_max"])
  
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
    return int(self.params["satiation"])
  
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
    return int(self.params["satiation_max"])
    
  @property
  def hydration(self):
    return int(self.params["hydration"])
  
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
    return int(self.params["hydration_max"])

  @property
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
      "mob_id": self.mob_id,
      "x": self.x, 
      "y": self.y,
      "z": self.z,
      "base_name": self.base_name,
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
      "knowledge": self.knowledge,
      "path": self.path_to_dest,
      "killable": self.killable,
      "can_duel": self.can_duel,
      "is_aggressive": self.is_aggressive,
      "can_ally": self.can_ally,
      "affiliation": self.affiliation
    }

  @classmethod
  def from_dict(cls, data):
    mob_id = data["mob_id"]
    if mob_id in cls.ids:
      raise ValueError(f"Duplicate mob ID found: {mob_id}")
    cls.ids[mob_id] = data["name"]


    eq = [Item.from_dict(item_data) for item_data in data["equipment"]]
    slots = data["slots"]
    for key in slots:
      if slots[key] == {}:
        slots[key] = None
      else:
        slots[key] = Item.from_dict(slots[key])
    
    try:
      mob = cls(mob_id, data["x"], data["y"], data["z"], data["base_name"], data["name"], data["alias"], data["description"], data["lvl"], data["exp"], data["weight"], data["money"], data["race"], data["proficiency"], data["params"], data["stats"], eq, slots, data["conversations"], data["knowledge"], data["path"], data["killable"], data["can_duel"],data["is_aggressive"], data["can_ally"], data["affiliation"])
      return mob
    except TypeError:
      print("Nie udało się wczytać danych.")
      print("Aktualnie ładowana postać: "+ data["name"])
      exit()