from world import World
from player import Player
from quest import Quest
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
    self.quests = []
  
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

  def load_game(self, path):
    data = MyJson.load_json("data/saves/"+path)
    self.player = Player.from_dict(data["player"])
    self.world = World.from_dict(data["world"])
    self.quests = [Quest.from_dict(data) for data in data["quests"]] 
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
    self.quests = [Quest.from_dict(data) for data in data["quests"]]
    self.player.current_location = self.world.locations[0]
    self.is_playing = True
    Konsola.clear()
    Konsola.print("Rozpocząłeś grę demonstracyjną", "lwhite")
    Konsola.hr()
    Helper.sleep(1)
    self.gameplay = Helper.get_new_gameplay_number()
  
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
    #are_you_sure = input()
    are_you_sure = "Y"
    if are_you_sure in ("Y", "y"):
      self.is_playing = False
      exit()
  
  def update_state(self):
    if self.player.quest_id:
      for quest in self.quests:
        if quest.id == self.player.quest_id:
          quest.status = 1
          self.player.quest_id = None
          Konsola.print(" Przyjąłeś zadanie: ", line_end="")
          Konsola.print(quest.name, "lyellow")
    
  def active_quests(self, quest_id=0):
    if not quest_id:
      Konsola.print("Twoje aktywne Questy", "lwhite")
      Konsola.hr()
      for quest in self.quests:
        if quest.status == 1:
          print(str(quest.id) + ". ", end="")
          Konsola.print(quest.name, "lyellow", line_end=" ")
          obj_count = 0
          obj_done = 0
          for obj in quest.objectives:
            obj_count += 1
            if obj["progress"] >= obj["amount"]:
              obj_done += 1

          print(" ( " + str(obj_done) + " / " + str(obj_count) + " )")
        #todo details about quest 
      Konsola.hr()
    else:
      for quest in self.quests:
        if quest.id == int(quest_id) and quest.status == 1:
          Konsola.print(quest.name, "lyellow")
          for obj in quest.objectives:
            color = "white"
            if obj["progress"] >= obj["amount"]:
              color = "lgreen"
            Konsola.print("  " + obj["name"], color, line_end=" ")
            print(" ( " + str(obj["progress"]) + " / " + str(obj["amount"]) + " )")
  def to_dict(self):
    return {
      "gameplay": self.gameplay, 
      "player": self.player.to_dict(),
      "world": self.world.to_dict(),
      "time_in_sec": self.time_in_sec,
      "quests": [quest.to_dict() for quest in self.quests]
    }

  @classmethod
  def from_dict(cls, data):
    world = World.from_dict(data["world"])
    player = Player.from_dict(data["player"])
    quests = [Quest.from_dict() for quest in data["quests"]]
    return cls(data["gameplay"], world, player, data["time_in_sec"], quests)
  
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