class Mob:
  def __init__(self, x, y, z, current_location, name, description, race, proficiency, hp, hp_max, mana, mana_max, strength, attack, defence):
    self.x = x
    self.y = y
    self.z = z
    self.current_location = current_location
    self.name = name
    self.description = description
    self.race = race
    self.proficiency = proficiency
    self.hp = hp
    self.hp_max = hp_max
    self.mana = mana
    self.mana_max = mana_max
    self.strength = strength
    self.attack = attack
    self.defence = defence

    self.equipment = []
    self.first_hand = None
    self.second_hand = None
    self.head = None
    self.body = None
    self.finger = None
    self.neck = None