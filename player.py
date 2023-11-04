from konsola import Konsola
from helper import Helper
from mob import Mob
from item import Item

class Player(Mob):
  def __init__(self, x, y, z, name, alias, description, lvl, race, proficiency, params, stats, equipment, slots, conversations, exp):
    super(Player, self).__init__(x, y, z, name, alias, description, lvl, race, proficiency, params, stats, equipment, conversations, slots)
    self.exp = exp

  def whoami(self):
    print("Jestem " + self.name + ", rasa: " + self.race + "\n" + self.description)
  def whereami(self):
    print("Znajduję się w "+self.current_location.name + ". Moje współrzędne to:")
    print("X: " + str(self.x))
    print("Y: " + str(self.y))
    print("Z: " + str(self.z))
  
  def max_exp_for_level(self, level):
    if level == 1:
      return 30
    else:
      return self.max_exp_for_level(level - 1) + 10 * (level - 1)
    
  def add_exp(self, exp):
    self.exp += exp
    while self.exp >= self.max_exp_for_level(self.level):
      self.lvl += 1
      self.exp -= self.max_exp_for_level(self.level)

  def move_in_direction(self, direction):
    if self.my_square().exits[direction]:
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
      self.my_square().show_square()
    else: print("Nie możesz tam przejść")
  
  def pick_up(self, item_name):
    item = super().pick_up(item_name)
    if item:
      Konsola.print("Podniosłeś ", line_end='')
      Konsola.print(item.name, "lwhite")
    else:
      Konsola.print("Nie ma tu takiej rzeczy", "red")
  
  def drop(self, item_name):
    item = super().drop(item_name)
    if item:
      Konsola.print("Upuściłeś ", line_end='')
      Konsola.print(item.name, "lwhite")
    else:
      Konsola.print("Nie masz takiej rzeczy w ekwipunku", "red")

  def see_item(self, item_name):
    item = Helper.find_item(self.equipment, item_name)
    if item:
      item.see_more()
      return 1
    item = Helper.find_item(self.my_square().items, item_name)
    if item:
      item.see_more()
      return 1
    Konsola.print("Nie ma tu takiej rzeczy, ani nie masz jej w ekwipunku", "red")
  
  def equip(self, item_name):
    item = super().equip(item_name)
    if item:
      print("Założyłeś " + item.name)
    else:
      Konsola.print("Nie masz takiej rzeczy w ekwipunku", "red")
  
  def outfit(self):
    Konsola.print("Twoje wyposarzenie", "lcyan")
    super().outfit()

  def navigate_conversation(self, current_step):
    options = current_step.get("options", [])
    if not options:
      return
    
    for option in options:
      Konsola.print(option["text"])
    
    choice = int(input(" > "))
    if 1 <= choice <= len(options):
      selected_option = options[choice - 1]
      Konsola.wrap(selected_option["response"], "lwhite")
      Helper.sleep(1)
      next_step = selected_option.get("next_step")
      if next_step:
        self.navigate_conversation(next_step)
      elif choice == len(options):
        return
      else:
        self.navigate_conversation(current_step)
    else:
      print("Błędny wybór")
      self.navigate_conversation(current_step)

  def talk_to(self, mob_name):
    mob = Helper.find_item(self.current_location.mobs, mob_name)
    if mob:
      if mob.conversations:
        Konsola.print(mob.conversations["greeting"], "lwhite")
        self.navigate_conversation(mob.conversations)


  def to_dict(self):
    player = super().to_dict()
    player["exp"] = self.exp
    return player
  
  @classmethod
  def from_dict(cls, data):
    eq = [Item.from_dict(item_data) for item_data in data["equipment"]]
    slots = data["slots"]
    for key in slots:
      if slots[key] == {}:
        slots[key] = None
      else:
        slots[key] = Item.from_dict(slots[key])
    
    return cls(data["x"], data["y"], data["z"], data["name"], data["alias"], data["description"], data["lvl"], data["race"], data["proficiency"], data["params"], data["stats"], eq, slots, data["conversations"], data["exp"])