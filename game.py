from world import World
from player import Player
from konsola import Konsola
from helper import Helper
from myjson import MyJson

class Game:
  def __init__(self, gameplay=1, player=None, world=None, time_in_sec=0):
    self.version = "0.0.0"
    self.gameplay = gameplay
    self.god_mode = True
    self.player = player
    self.world = world
    self.is_playing = False
    self.time_in_sec = time_in_sec
  
  def title_screen(self):
    method_map = {
      "2": self.choose_save,
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

  def choose_save(self):
    saves = Helper.open_saves()
    if not saves:
      Konsola.print("Nie masz żadnych zapisów", "lred")
      return
    
    number = 1
    for path in saves:
      path = path.rsplit( ".", 1 )[ 0 ]
      print(str(number) + ". ", end="")
      Konsola.print(path, "lwhite")
      number+=1

    Konsola.print("Wybierz zapis: ", "lgreen")
    correct = False
    while not correct:
      choice = input()
      try:
        choice = int(choice)
      except:
        print("Podaj liczbę ")
        continue
      if 0 < choice <= len(saves):
        self.load_game(saves[choice-1])
        return
      else:
        print("Nie ma takiego zapisu ")

  def load_game(self, path):
    data = MyJson.load_json("data/saves/"+path)
    self.player = Player.from_dict(data["player"])
    self.world = World.from_dict(data["world"])
     
    self.player.current_location = self.world.locations[0]
    self.is_playing = True
    Konsola.clear()
    Konsola.print("Udało Ci się wczytać grę", "lwhite")
    Konsola.hr()
    Helper.sleep(1)

  def demo(self):
    data = MyJson.load_json("data/init/demo.json")
    self.player = Player.from_dict(data["player"])
    self.world = World.from_dict(data["world"])
     
    self.player.current_location = self.world.locations[0]
    self.is_playing = True
    Konsola.clear()
    Konsola.print("Rozpocząłeś grę demonstracyjną", "lwhite")
    Konsola.hr()
    Helper.sleep(1)
  
  def save(self):
    data = self.to_dict()
    location_name = self.player.current_location.name
    datetime = Helper.datetime()
    path = 'data/saves/' + datetime + "_" + location_name + "_" + str(self.gameplay) + '.json'
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