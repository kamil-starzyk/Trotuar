from mob import Mob

class Player(Mob):
  def __init__(self, x, y, name, description, race, proficiency, hp, hp_max, mana, mana_max, strength, attack, defence, exp, lvl, satiation, satiation_max, hydration, hydration_max):
    super(Player, self).__init__(x, y, name, description, race, proficiency, hp, hp_max, mana, mana_max, strength, attack, defence)
    self.exp = exp
    self.lvl = lvl
    self.satiation = satiation
    self.satiation_max = satiation_max
    self.hydration = hydration
    self.hydration_max = hydration_max

  def whoami(self):
    print("Jestem " + self.name + ", rasa: " + self.race + "\n" + self.description)
  
  def max_exp_for_level(self, level):
    if level == 1:
      return 30
    else:
      return max_exp_for_level(level - 1) + 10 * (level - 1)
    
  def add_exp(self, exp):
    self.exp += exp
    while self.exp >= self.max_exp_for_level(self.level):
      self.lvl += 1
      self.exp -= self.max_exp_for_level(self.level)
