from world import World
from player import Player
from konsola import Konsola
from helper import Helper
from myjson import MyJson

class Game:
  def __init__(self, gameplay=0, player=None, world=None, time_in_sec=0):
    self.version = "0.0.0"
    self.gameplay = gameplay
    self.god_mode = True
    self.player = player
    self.world = world
    self.is_playing = False
    self.time_in_sec = time_in_sec
  
  def title_screen(self):
    method_map = {
      
      "3": self.demo,
      "5": self.end_game,
    }

    Konsola.show_title_screen(self.version)
    while not self.is_playing:
      choice = input()
      if choice in method_map:
        method_map[choice]()
      else:
        print("Wprowadź poprawny wybór")


  def demo(self):
    data = MyJson.load_json("data/init/demo.json")
    self.player = Player.from_dict(data["player"])
    self.world = World.from_dict(data["world"])
     
    self.player.current_location = self.world.locations[0]
    self.is_playing = True
  
  def save(self):
    data = self.to_dict()
    location_name = self.player.current_location.name
    datetime = Helper.datetime()
    path = 'data/save/' + datetime + "_" + location_name + "_" + str(self.gameplay) + '.json'
    path = path.lower()
    path = path.replace(" ", "_")
    print(path)
    MyJson.save_json(path, data)

  def end_game(self):
    print("Czy na pewno chcesz wyjść? Upewnij się, że zapisałeś grę (Y/N)")
    are_you_sure = input()
    if are_you_sure in ("Y", "y"):
      self.is_playing = False
      exit()
  

  def to_dict(self):
    return {
      "gameplay": self.gameplay, 
      "player": self.player.to_dict(),
      "world": self.world.to_dict(),
      "time_in_sec": self.time_in_sec
    }

  @classmethod
  def from_dict(cls, data):
    world = World.from_dict(data["world"])
    player = Player.from_dict(data["player"])
    return cls(data["gameplay"], world, player, data["time_in_sec"])