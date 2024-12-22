from konsola import Konsola
from helper import Helper
from player import Player
from activity import Activity
from random import shuffle


class Combat:
  def __init__(self):
    self.combatants = []
    self.queue = []
    self.active = True    

  def add_combatant(self, mob):
    if mob not in self.combatants:
      self.combatants.append(mob)






    