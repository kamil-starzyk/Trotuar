from konsola import Konsola
from helper import Helper
from mob import Mob
from item import Item

class Player(Mob):
  def __init__(self, x, y, z, name, alias, description, lvl, money, race, proficiency, params, stats, equipment, slots, conversations, knowledge, exp):
    super(Player, self).__init__(x, y, z, name, alias, description, lvl, money, race, proficiency, params, stats, equipment, slots, conversations, knowledge)
    self.exp = exp
    self.quest_id = None
    self.picked_item = None
    self.droped_item = None
    self.given_item = None
    self.item_receiver = None

  def whoami(self):
    print("Jestem " + self.name + ", rasa: " + self.race + "\n" + self.description)
    print("Poziom: " + str(self.lvl) + " ( " + str(self.exp) + " / " + str(self.max_exp_for_level(self.lvl)) + " )")

  def whereami(self):
    print("Znajduję się w "+self.current_location.name + ". Moje współrzędne to:")
    print('"x": ' + str(self.x)+',')
    print('"y": ' + str(self.y)+',')
    print('"z": ' + str(self.z))
  
  def max_exp_for_level(self, level):
    if level == 1:
      return 30
    else:
      return self.max_exp_for_level(level - 1) + 10 * (level - 1)
    
  def add_exp(self, exp):
    self.exp += exp
    while self.exp >= self.max_exp_for_level(self.lvl):
      self.lvl += 1
      Konsola.print(" >> Gratulacje! Osiągnąłeś kolejny poziom główny ( " + str(self.lvl) + " ) <<", "lgreen")
      self.exp -= self.max_exp_for_level(self.lvl-1)

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
      self.my_square().show_square()
    else: print("Nie możesz tam przejść")
  
  def pick_up(self, item_name):
    item = super().pick_up(item_name)
    if item:
      self.picked_item = item
      Konsola.print("Podniosłeś ", line_end='')
      Konsola.print(item.name, "lwhite")
    else:
      Konsola.print("Nie ma tu takiej rzeczy", "red")
  
  def drop(self, item_name):
    item = super().drop(item_name)
    if item:
      self.droped_item = item
      Konsola.print("Upuściłeś ", line_end='')
      Konsola.print(item.name, "lwhite")
    else:
      Konsola.print("Nie masz takiej rzeczy w ekwipunku", "red")
  
  def give(self, item_name):
    item = Helper.find_item(self.equipment, item_name)
    if item:
      mobs = self.current_location.mobs_on_square(self.my_square())
      mob = None
      if len(mobs) == 1:
        mob = mobs[0]
      else:
        Konsola.print("Komu chcesz przekazać " + item.name +"?", "lcyan", line_end=' ')
        mob_name = input()
        mob = Helper.find_item(mobs, mob_name)
      if mob:
        if item.stackable() and item.amount > 1:
          print("Jaką ilość chcesz podarować? (max: " + str(item.amount) + ")")
          amount_to_give = Konsola.int_input(1, item.amount)
          if amount_to_give == item.amount:
            self.equipment.remove(item)
          else:
            item = Item.unstack(item, amount_to_give)
        else:
          self.equipment.remove(item)

        mob.equipment.append(item)
        self.item_receiver = mob
        self.given_item = item
        return item
      else:
        Konsola.print("Nie udało się przekazać przedmiotu", "red")

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
    options = []
    for option in current_step.get("options", []):
      condition = option.get("condition")
      if condition is None or self.knowledge.get(condition, False):
        options.append(option)

    if not options:
      return
    
    number = 1
    for option in options:
      Konsola.print(" (" + str(number) + ".) " + option["text"])
      number+=1
      
    choice = Konsola.int_input()
    if 1 <= choice <= len(options):
      selected_option = options[choice - 1]
      Konsola.wrap(selected_option["response"], "lwhite")
      if selected_option.get("knowledge"):
        for key, value in selected_option["knowledge"].items():
          if key not in self.knowledge:
            self.knowledge[key] = value
      if selected_option.get("forget"):
        key = selected_option.get("forget")
        if key in self.knowledge:
          del self.knowledge[key]
          
      if "quest_id" in selected_option:
        quest_id = selected_option["quest_id"]
        self.quest_id = quest_id
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
    mobs = self.current_location.mobs_on_square(self.my_square())
    mob = Helper.find_item(mobs, mob_name)
    if mob: 
      if self.my_square() == mob.my_square():
        if mob.conversations:
          Konsola.print(mob.conversations["greeting"], "lwhite")
          self.navigate_conversation(mob.conversations)
  
  def use_passage(self, direction):
    passages = self.current_location.secret_passages
    for p in passages:
      if p["x"] == self.x and p["y"] == self.y and p["z"] == self.z:
        if p["direction"] == direction and p["condition"] in self.knowledge:
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
          print("Skorzystałeś z tajnego przejścia")
          Helper.sleep(1)
          self.my_square().show_square()
          return
    print("Chyba nie tędy droga...")
      

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
    
    return cls(data["x"], data["y"], data["z"], data["name"], data["alias"], data["description"], data["lvl"], data["money"],data["race"], data["proficiency"], data["params"], data["stats"], eq, slots, data["conversations"], data["knowledge"], data["exp"])