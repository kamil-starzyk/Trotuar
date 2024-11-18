from helper import Helper
from konsola import Konsola
from item import Item
from utility import Utility
from activity import Activity
from blueprint import Blueprint
from equipment import Equipment
import math #ceil damage
import random #for escape

class Npc:
  BASIC_CARRY_WEIGHT = 40
  ids = {}
  def __init__(self, mob_id, x, y, z, base_name, name, alias, description, lvl, exp, weight, money, race, proficiency, params, stats, skills, equipment, slots, conversations, knowledge, journal, current_activity, next_activity, schedule, area, path, can_trade, items_to_sell, wants_to_buy, killable, can_duel, is_aggressive, can_ally, teacher_of, blueprints, affiliation):
    super(Npc, self).__init__(mob_id, x, y, z, base_name, name, alias, description, lvl, exp, weight, money, race, proficiency, params, stats, skills, equipment, slots, knowledge, journal)
    self.conversations = conversations
    
    
    self.current_activity = current_activity 
    self.next_activity = next_activity
    self.schedule = schedule
    self.area = area
    self.dest_x = None
    self.dest_y = None
    self.dest_z = None
    self.is_following_route = False
    self.path_to_dest = path
    
    self.can_trade = can_trade
    self.items_to_sell = items_to_sell
    self.wants_to_buy = wants_to_buy
    self.chance_bonus = 0
    self.killable = killable
    self.can_duel = can_duel
    self.is_aggressive = is_aggressive
    self.can_ally = can_ally
    self.teacher_of = teacher_of
    self.blueprints = blueprints
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
  


  def add_destination(self, x, y, z):
    if self.current_location.find_square(x, y, z):
      self.dest_x = x
      self.dest_y = y
      self.dest_z = z
      self.is_following_route = True
      return True
    print("There is no square with this coordinates")
    return 0
  
  def calculate_next_position(self, direction):
    # Extract logic for calculating next coordinates based on direction
    next_x, next_y, next_z = self.x, self.y, self.z

    if direction == "n":
        next_y -= 1
    elif direction == "e":
        next_x += 1
    elif direction == "s":
        next_y += 1
    elif direction == "w":
        next_x -= 1
    elif direction == "u":
        next_z += 1
    elif direction == "d":
        next_z -= 1

    return next_x, next_y, next_z

  def move_in_direction(self, direction):
    next_x, next_y, next_z = self.calculate_next_position(direction)

    # Check if the next coordinates are within the allowed area before moving
    # if self.area and {"x": next_x, "y": next_y, "z": next_z} in self.area.squares:
    if direction in self.my_square.exits:
      self.x = next_x
      self.y = next_y
      self.z = next_z
      if self.overloaded:
        stamina = -20*self.overloaded
        stamina_max = -0.2 - (4*self.overloaded)
        self.adjust_stamina(stamina, stamina_max)
      else:
        self.adjust_stamina(0.5, -0.2)
      return direction
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
    
    self.is_following_route = False
    return None

  def call_for_help(self):
    try:
      allies = self.find_mobs_in_radius(5, affiliation=self.affiliation[0])
      for a in allies:
        a.find_path_to_coordinates(self.x, self.y, self.z)
      return len(allies)
    except IndexError:
      return 0
    
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
    exits = []
    for e in self.my_square.exits:
      next_x, next_y, next_z = self.calculate_next_position(e)

      # Check if the next coordinates are within the allowed area before moving
      if self.area and {"x": next_x, "y": next_y, "z": next_z} in self.area.squares:
        exits.append(e)
    if not exits:
      return
    
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
        
  def update_current_activity(self, time):
    current_time = time.get_hour_minute()
    current_week_day = time.get_week_day()
    for activity_day, activities in self.schedule.items():
      for activity_time, activity in activities.items():
        if activity_time == current_time and int(activity_day) == int(current_week_day):
          try:
            if self.current_activity.type == "fight":
              enemy = next((mob for mob in self.current_location.mobs if mob.mob_id == mob.current_activity.mob_id), None)
              if enemy:
                enemy.current_activity = enemy.next_activity
                enemy.next_activity = None
          except AttributeError:
            pass

          self.current_activity = activity

  

    

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
    return self.params["stamina_total"]/2
    
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
  def carry_weight(self):
    strength_coefficient = self.stat_coefficient(self.stats["strength"])
    return int(strength_coefficient*Mob.BASIC_CARRY_WEIGHT)
  
  @property
  def max_carry_weight(self):
    carry_weight = self.carry_weight
    endurance_coefficient = self.stat_coefficient(self.stats["endurance"])
    endurance_bonus_weight = 0.75*endurance_coefficient*Mob.BASIC_CARRY_WEIGHT
    return int(carry_weight + endurance_bonus_weight)

  @property
  def weight_carried_rn(self):
    total_weight = sum(item.weight*item.amount for item in self.equipment)
    return total_weight
  
  @property
  def overloaded(self):
    """
    Overloaded informs about carrying more weight than carry_weight but less than max_carry_weight.
    If mob carries less than carry_weight it will return 0, otherwise it will return fraction of weight over carry_weight / max_carry_weight
    Range of this value is 0-1
    Returns:
        float: fraction of excessive weight.
    """
    excessive_weight = max(0, self.weight_carried_rn - self.carry_weight)
    fraction = excessive_weight / self.max_carry_weight
    return fraction

  @property
  def my_square(self):
    return self.current_location.find_square(self.x, self.y, self.z)


  def to_dict(self):
    npc = super().to_dict()
    return npc
  
  @classmethod
  def from_dict(cls, data):
    mob_id = data["mob_id"]
    if mob_id in cls.ids:
      raise ValueError(f"Duplicate mob ID found: {mob_id}")
    cls.ids[mob_id] = data["name"]


    eq = Equipment.from_dict(data["equipment"])
    slots = data["slots"]
    for key in slots:
      if slots[key] == {}:
        slots[key] = None
      else:
        slots[key] = Item.from_dict(slots[key])
    items_to_sell = [Item.from_dict(item_data) for item_data in data["items_to_sell"]]
    
    schedule_data = data.get("schedule", {})
    schedule = {str(day): {} for day in range(1, 8)} 
    for days_key, activities in schedule_data.items():
      for day in days_key:
        for time, activity_data in activities.items():

          if time not in schedule[day]:
            schedule[day][time] = Activity.from_dict(activity_data)
          
    # print(schedule)
    
    current_activity = Activity.from_dict(data.get("current_activity")) if data["current_activity"] else None
    next_activity = Activity.from_dict(data.get("next_activity")) if data["next_activity"] else None
    blueprints = [Blueprint.from_dict(blueprint) for blueprint in data["blueprints"]]

    try:
      mob = cls(mob_id, data["x"], data["y"], data["z"], data["base_name"], data["name"], data["alias"], data["description"], data["lvl"], data["exp"], data["weight"], data["money"], data["race"], data["proficiency"], data["params"], data["stats"], data["skills"], eq, slots, data["conversations"], data["knowledge"], data["journal"], current_activity, next_activity, schedule, data["area"], data["path"], data["can_trade"], items_to_sell, data["wants_to_buy"], data["killable"], data["can_duel"], data["is_aggressive"], data["can_ally"], data['teacher_of'], blueprints, data["affiliation"])
      return mob
    except TypeError:
      print("Nie udało się wczytać danych: TypeError")
      print("Aktualnie ładowana postać: "+ data["name"])
      exit()
    except KeyError:
      print("Nie udało się wczytać danych: KeyError")
      print("Aktualnie ładowana postać: "+ data["name"])
      exit()