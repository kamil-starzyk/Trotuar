from konsola import Konsola
from helper import Helper
from mob import Mob

class Player(Mob):
  def __init__(self, x, y, z, current_location, name, description, race, proficiency, hp, hp_max, mana, mana_max, strength, attack, defence, exp, lvl, satiation, satiation_max, hydration, hydration_max):
    super(Player, self).__init__(x, y, z, current_location, name, description, race, proficiency, hp, hp_max, mana, mana_max, strength, attack, defence)
    self.exp = exp
    self.lvl = lvl
    self.satiation = satiation
    self.satiation_max = satiation_max
    self.hydration = hydration
    self.hydration_max = hydration_max

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