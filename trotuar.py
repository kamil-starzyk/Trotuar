class Mob:
  def __init__(self, x, y, name, description, race, hp, mana, strength, attack, defence):
    self.x = x
    self.y = y
    self.name = name
    self.description = description
    self.race = race
    self.hp = hp
    self.hp_max = hp
    self.mana = mana
    self.mana_max = mana
    self.strength = strength
    self.attack = attack
    self.defence = defence
    self.equipment = []
  
class Player(Mob):
  def __init__(self, x, y, name, description, race, hp, mana, strength, attack, defence):
    super(Player, self).__init__(x, y, name, description, race, hp, mana, strength, attack, defence)

  def whoami(self):
    print("Jestem " + self.name + ", rasa: " + self.race + "\n" + self.description)

class Square:
  def __init__(self, x, y, z, name, description, exit_n, exit_e, exit_s, exit_w, exit_u, exit_d):
    self.x = x
    self.y = y
    self.z = z
    self.name = name
    self.description = description
    self.exit_n = exit_n
    self.exit_e = exit_e
    self.exit_s = exit_s
    self.exit_w = exit_w
    self.exit_u = exit_u
    self.exit_d = exit_d

class Location:
  def __init__(self, name, size_x, size_y, size_z):
    self.name = name
    self.size_x = size_x
    self.size_y = size_y
    self.size_z = size_z
    self.squares = []

user_choice = input()

