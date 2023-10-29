from world import World
from square import Square
from mob import Mob
from player import Player
from konsola import Konsola
from myjson import MyJson

class Game:
	def __init__(self):
		self.version = "0.0.0"
		self.gameplay = 0
		self.god_mode = True
		self.world = None
		self.player = None
		self.is_playing = False
		self.time_in_sec = 0
	
	def title_screen(self):
		method_map = {
			"1": self.new_game,
			"5": self.end_game,
		}

		Konsola.show_title_screen(self.version)
		while not self.is_playing:
			choice = input()
			if choice in method_map:
				method_map[choice]()
			else:
				print("Wprowadź poprawny wybór")


	def new_game(self):
		data = MyJson.load_json("data/init/world.json")
		self.world = World.from_dict(data)
		current_location = self.world.locations[0]
		self.player = Player(0,0,0, current_location, "Jozin", "z Bazin", "hooman", "warrior", 90, 100, 5, 5, 10, 10, 10, 0, 1, 90, 100, 70, 100)
		self.is_playing = True
	

	def end_game(self):
		self.is_playing = False
		print("Czy na pewno chcesz wyjść? Upewnij się, że zapisałeś grę (Y/N)")
		are_you_sure = input()
		are_you_sure = "Y"
		if are_you_sure in ("Y", "y"):
			exit()