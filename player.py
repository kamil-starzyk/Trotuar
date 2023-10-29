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
    current_square = self.current_location.find_square(self.x, self.y, self.z)
    if current_square.exits[direction]:
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
      current_square = self.current_location.find_square(self.x, self.y, self.z)
      current_square.show_square()
    else: print("Nie możesz tam przejść")