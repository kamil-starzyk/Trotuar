from world import World
from square import Square
from mob import Mob
from player import Player
from myjson import MyJson

class Game:
	def __init__(self):
		self.version = "0.0.0"
		self.gameplay = 0
		self.god_mode = True
		self.world = None
		self.hero = None
		self.is_playing = False
		self.time_in_sec = 0
	
	