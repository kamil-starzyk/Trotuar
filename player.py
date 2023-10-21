from mob import Mob

class Player(Mob):
  def __init__(self, x, y, name, description, race, hp, mana, strength, attack, defence):
    super(Player, self).__init__(x, y, name, description, race, hp, mana, strength, attack, defence)

  def whoami(self):
    print("Jestem " + self.name + ", rasa: " + self.race + "\n" + self.description)
