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
    params = {
      "hp": 100,
      "hp_max": 100,
      "mana": 5,
      "mana_max": 5,
      "satiation": 80,
      "satiation_max": 100,
      "hydration": 50,
      "hydration_max": 100
    }
    stats = {
      "strength": 30,
      "attack": 15,
      "defence": 25
    }
    equipment =[]
    slots = {
      "first_hand" : {},
      "second_hand" : {},
      "head" : {},
      "body" : {},
      "finger" : {},
      "neck" : {}
    }
    conversations = {}
     
    self.player = Player(2,2,0, "Alwer", ["alwer"], "to ty ", "Człowiek", "Wojownik", 1, params, stats, equipment, slots, conversations, 0 )
    self.player.current_location = self.world.locations[0]
    self.is_playing = True
  

  def end_game(self):
    print("Czy na pewno chcesz wyjść? Upewnij się, że zapisałeś grę (Y/N)")
    are_you_sure = input()
    if are_you_sure in ("Y", "y"):
      self.is_playing = False
      exit()