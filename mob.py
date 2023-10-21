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