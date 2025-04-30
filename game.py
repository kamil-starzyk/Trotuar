from gametime import GameTime
from world import World
from player import Player
from quest import Quest
from konsola import Konsola
from helper import Helper
from myjson import MyJson
from activity import Activity

class Game:
  def __init__(self, gameplay=1, player=None, world=None, milestones=[]):
    self.version = "0.0.0"
    self.gameplay = gameplay
    self.god_mode = True
    self.player = player
    self.world = world
    self.is_playing = False
    self.quests = []
    self.time = None
    self.milestones = milestones #milestone["status"] = 0 - not active / 1 - active / 2 - completed
  
  def title_screen(self):
    method_map = {
      "1": self.new_game,
      "2": self.choose_save,
      "3": self.demo,
      "5": self.end_game,
      "q": self.end_game,
    }

    Konsola.show_title_screen(self.version)
    while not self.is_playing:
      choice = input("Wybierz tryb gry: ")
      if choice in method_map:
        method_map[choice]()
      else:
        Konsola.print("Wprowadź poprawny wybór", "red")

  def new_game(self):
    Konsola.print("Ten tryb jeszcze nie jest dostępny :(", "red")
    Konsola.print("Aby poczuć przedsmak pełnej rozgrywki spróbuj zagrać w ", line_end="")
    Konsola.print("DEMO", "lwhite")

  def load_game(self, path):
    data = MyJson.load_json("data/saves/"+path)
    self.player = Player.from_dict(data["player"])
    self.player.game = self
    self.world = World.from_dict(data["world"])
    self.time = GameTime.from_dict(data["time"])
    self.quests = [Quest.from_dict(data) for data in data["quests"]]
    self.milestones = data["milestones"] 
    self.player.current_location = self.world.locations[0]
    self.player.area = self.world.locations[0].areas[0]
    self.is_playing = True
    Konsola.clear()
    Konsola.print("Udało Ci się wczytać grę", "lwhite")
    Konsola.hr()
    Helper.sleep(1)

  def demo(self):
    data = MyJson.load_json("data/init/demo.json")
    self.player = Player.from_dict(data["player"])
    self.player.game = self
    self.world = World.from_dict(data["world"])
    self.time = GameTime.from_dict(data["time"])
    self.quests = [Quest.from_dict(data) for data in data["quests"]]
    self.milestones = data["milestones"]
    self.player.current_location = self.world.locations[0]
    self.is_playing = True
    Konsola.clear()
    #Konsola.print("Rozpocząłeś grę demonstracyjną", "lwhite")
    Konsola.wrap("Wszystko się nagle zachwiało i obudziłeś się z drzemki. To nie dom się wali, po prostu łódź się zakołysała.")
    #Helper.sleep(1)
    Konsola.wrap("Ah tak... zostawiłeś rodzinny dom i wioskę daleko za sobą. Podczas podróży przysnąłeś siedząc na skrzyni, oparty o jutowy worek. Spławiacz Jacek zgodził się Ciebie zabrać za drobną opłatą i teraz płyniecie razem na południe. Po drodze jest miasto Torenberg, tam zamierzasz wysiąść i szukać przygód.")
    #Helper.sleep(3)
    Konsola.wrap("Szum wody...")
    #Helper.sleep(0.5)
    Konsola.wrap("Kołysanie łodzi...")
    #Helper.sleep(0.5)
    Konsola.wrap("\"To już niedaleko\" - mówi nagle Jacek. Rozglądasz się i faktycznie, widzisz w oddali ponad koronami drzew wieże wznoszące się nad murami.")
    #Helper.sleep(1)
    Konsola.wrap("Mija jeszcze kilka chwil, po których dobijacie do brzegu. Jacek wyskakuje z łodzi i cumuje ją do palika. Ty tymczasem wychodzisz na brzeg.")
    Konsola.hr()
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


  def show_current_square(self):
    self.player.my_square.show_square()


  def update_state(self, sec):
    self.update_quests()
    self.check_player_status()
    self.update_mobs(sec)
    self.process_milestones()

  def update_quests(self):
    for quest in self.quests:
      if self.player.quest_id:
        if quest.id == self.player.quest_id:
          quest.status = 1
          Konsola.print(" Przyjąłeś zadanie: ", line_end="")
          Konsola.print(quest.name, "lyellow")
    
    for quest in [q for q in self.quests if q.status == 1]:
      if self.player.picked_item:
        for obj in quest.objectives:
          if obj["type"] == "item_in_eq" and obj["item"] == self.player.picked_item.name:
            obj["progress"] += self.player.picked_item.amount
            if obj["progress"] <= obj["amount"]:
              Konsola.print(" Postęp w zadaniu: ", line_end="")
              Konsola.print(quest.name, "lyellow")
      
      if self.player.item_receiver:
        for obj in quest.objectives:
          if obj["type"] == "return_item" and obj["npc"] == self.player.item_receiver.name and obj["item"] == self.player.given_item.name:
            obj["progress"] += self.player.given_item.amount
            if obj["progress"] <= obj["amount"]:
              Konsola.print(" Postęp w zadaniu: ", line_end="")
              Konsola.print(quest.name, "lyellow")

      if self.player.droped_item:
        for obj in quest.objectives:
          if obj["type"] == "item_in_eq" and obj["item"] == self.player.droped_item.name:
            if obj["progress"] >= self.player.droped_item.amount:
              obj["progress"] -= self.player.droped_item.amount
            else:
              obj["progress"] = 0
      
      if self.player.mobs_killed:
        for obj in quest.objectives:
          for mob in self.player.mobs_killed:
            if obj["type"] == "mobs_killed" and obj["npc"] == mob.base_name:
              obj["progress"] += 1
              if obj["progress"] <= obj["amount"]:
                Konsola.print(" Postęp w zadaniu: ", line_end="")
                Konsola.print(quest.name, "lyellow")
      
      if self.player.talk_to_npc:
        for obj in quest.objectives:
            if obj["type"] == "talk_to_npc" and obj["npc"] == self.player.talk_to_npc:
              obj["progress"] += 1
              if obj["progress"] <= obj["amount"]:
                Konsola.print(" Postęp w zadaniu: ", line_end="")
                Konsola.print(quest.name, "lyellow")
      
      if quest.is_finished():
        quest.status = 2
        Konsola.print(" Ukończyłeś zadanie : ", line_end="")
        Konsola.print(quest.name, "lgreen")
        #Helper.sleep(1)
        if "money" in quest.reward:
          Konsola.print("  Otrzymujesz: ", line_end="")
          Konsola.print(str(quest.reward["money"]) + " złota", "lyellow")
          self.player.money += quest.reward["money"]
        if "exp" in quest.reward:
          Konsola.print("  Otrzymujesz: ", line_end="")
          Konsola.print(str(quest.reward["exp"]) + " doświadczenia", "lyellow")
          self.player.add_exp(quest.reward["exp"])
        key = quest.name
        if key in self.player.knowledge:
          del self.player.knowledge[key]
        self.player.knowledge[quest.knowledge_entry] = "Benc"
    self.player.quest_id = None
    self.player.picked_item = None
    self.player.droped_item = None
    self.player.given_item = None
    self.player.item_receiver = None
    self.player.mobs_killed = []
  
  def check_player_status(self):
    if self.player.hp == 0:
      self.is_playing = False
      Konsola.you_died()
      #Helper.sleep(2)
      print("")
      Konsola.hr()
      print("[1] Wróć do menu")
      print("[2] Opuść grę")
 
      choice = Konsola.int_input(1,2)
      if choice == 2:
        exit()

  def update_mobs(self, sec):
    mobs = self.player.current_location.mobs

    seconds = int(sec)
    minutes = seconds // 60
    
    def loop_body():
      for mob in mobs:
        if not mob.current_activity:
          continue
        mob.update_current_activity(self.time)
        is_mob_on_square = True if mob.my_square == self.player.my_square else False
        if mob.current_activity.type in ["random_walk", "following_path"]:
          try:
            direction = mob.follow_path()
            if not direction:
              direction = mob.random_walk()
            #direction = None
          except AttributeError:
            print(mob.mob_id)
            print(f'{mob.x} : {mob.y} : {mob.z}')
          if is_mob_on_square and direction:
            to_direction = Konsola.direction_translator(direction)
            Konsola.print("  " + mob.name + " odszedł " + to_direction, "magenta")
          if direction and mob.my_square == self.player.my_square:
            from_direction = Konsola.direction_translator(direction, True)
            Konsola.print("  " + mob.name + " przyszedł " + from_direction, "lmagenta")
        
        if mob.current_activity.type == "following_path":
          x, y, z = mob.current_activity.destination.values()
          if mob.is_on_square(x, y, z):
            mob.current_activity = mob.next_activity
            mob.next_activity = None
  
        elif mob.current_activity.type == "random_walk":
          area_name = mob.current_activity.area
          destined_area = mob.current_location.find_area(area_name)
          mob.area = destined_area
          if not destined_area.are_coordinates_in_area(mob.x, mob.y, mob.z):
            x = destined_area.reference_coordinate["x"]
            y = destined_area.reference_coordinate["y"]
            z = destined_area.reference_coordinate["z"]
            mob.find_path_to_coordinates(x, y, z)
            mob.next_activity = mob.current_activity
            mob.current_activity = Activity("following_path", ["podąża gdzieś wesołym krokiem", "idzie gdzieś podśpiewując"], 6, destination= {"x": x, "y": y, "z": z})
            continue

        elif mob.current_activity.type == "stays_at_place":
          x, y, z = mob.current_activity.destination.values()
          if not mob.is_on_square(x, y, z):
            mob.find_path_to_coordinates(x, y, z)
            mob.next_activity = mob.current_activity
            mob.current_activity = Activity("following_path", ["podąża gdzieś wesołym krokiem", "idzie gdzieś podśpiewując"], 6, destination= {"x": x, "y": y, "z": z})
            continue



        elif mob.current_activity.type == "fight":
          enemy = next((m for m in self.player.current_location.mobs if m.mob_id == mob.current_activity.mob_id), None)
          if not enemy:
            continue
          if not mob.is_on_square(enemy.x, enemy.y, enemy.z):
            mob.find_path_to_coordinates(enemy.x, enemy.y, enemy.z)
            mob.next_activity = mob.current_activity
            mob.current_activity = Activity("following_path", ["podąża gdzieś z groźną miną"], 6, destination= {"x": enemy.x, "y": enemy.y, "z": enemy.z})
            
          if enemy.current_activity:
            if enemy.current_activity.type != "fight":
              enemy.next_activity = enemy.current_activity
              enemy.current_activity = Activity("fight", "walczy z "+mob.name, 5, mob.mob_id)
          mob.try_to_draw_weapon(is_mob_on_square)
          mob.perform_attack(enemy, "hit", is_mob_on_square)

    for _ in range(minutes):
      loop_body()

      self.time.time_progress(60)
      seconds -= 60
    
    if seconds > 0:
      chance = Helper.random(0, 60)
      if chance + seconds > 60:
        loop_body()
      self.time.time_progress(seconds)

  def process_milestones(self):
    for _, milestone in self.milestones.items():
      conditions_met = True
      if milestone["status"] == 1 and milestone["conditions"]:
        for condition in milestone["conditions"]:
          if condition["type"] == "quest_objective_done":
            quest = next((q for q in self.quests if q.id == condition["quest_id"]), None)
            if quest.status < 1:
              conditions_met = False
            else:
              for obj in quest.objectives:
                if obj["name"] == condition["objective_name"] and obj["progress"] == obj["amount"]:
                  conditions_met = True
                  break
                else:
                  conditions_met = False
            
          if condition["type"] == "player_on_square":
            x = condition["x"]
            y = condition["y"]
            z = condition["z"]
            if not (self.player.current_location.name == condition["location"] and self.player.is_on_square(x,y,z)):
              conditions_met = False
              break
          if condition["type"] == "player_overloaded":
            if not self.player.overloaded:
              conditions_met = False
              break

            

      if milestone["status"] == 1 and conditions_met:
        for action in milestone["actions"]:
          if action["type"] == "wrap_text":
            Konsola.wrap(action["text"])
            Konsola.hr()
            #Helper.sleep(1)

          elif action["type"] == "take_drop_item":
            mob = next((mob for mob in self.player.current_location.mobs if mob.mob_id == action["mob_id"]), None)
            mob.take(action["item_name"])
            mob.drop(action["item_name"], action["item_amount"])
            Konsola.print(action["message"], "lmagenta")
            #Helper.sleep(1.5)
          
          elif action["type"] == "load_passenger":
            mob = next((mob for mob in self.player.current_location.mobs if mob.mob_id == action["mob_id"]), None)
            utility = next((utility for utility in self.player.my_square.utilities if utility.id == action["utility_id"]), None)
            if "passengers" in utility.attr:
              if utility.add_passenger(mob):
                Konsola.print(action["message"], "lmagenta")
              else:
                Konsola.print("Nie udało się wsiąść", "red")
          
          elif action["type"] == "unload_passenger":
            utility = next((utility for utility in self.player.my_square.utilities if utility.id == action["utility_id"]), None)
            if "passengers" in utility.attr:
              if utility.remove_passenger(action["mob_id"], self.player.my_square):
                Konsola.print(action["message"], "lmagenta")
              else:
                Konsola.print("Nie udało się wysiąść", "red")


            
        Helper.sleep(1.5)
        self.show_current_square()

        milestone["status"] = 2
        if milestone["next_milestone"]:
          self.milestones[milestone["next_milestone"]]["status"] = 1



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
          Konsola.wrap(quest.description)
          Konsola.hr()
          for obj in quest.objectives:
            color = "white"
            if obj["progress"] >= obj["amount"]:
              color = "lgreen"
            Konsola.print("  " + obj["name"], color, line_end=" ")
            print(" ( " + str(obj["progress"]) + " / " + str(obj["amount"]) + " )")
          quest.print_reward()

  def to_dict(self):
    return {
      "gameplay": self.gameplay, 
      "player": self.player.to_dict(),
      "world": self.world.to_dict(),
      "time": self.time.to_dict(),
      "quests": [quest.to_dict() for quest in self.quests],
      "milestones": self.milestones
    }

  @classmethod
  def from_dict(cls, data):
    world = World.from_dict(data["world"])
    time = GameTime.from_dict(data["time"])
    player = Player.from_dict(data["player"])
    quests = [Quest.from_dict() for quest in data["quests"]]
    milestones = data["milestones"]
    return cls(data["gameplay"], world, player, time, quests, milestones)
  
  def choose_save(self):
    saves = Helper.open_saves()
    if not saves:
      Konsola.print("Nie masz żadnych zapisów", "lred")
      return
    
    number = 1
    Konsola.print("  Dostępne zapisy:  ", "black", "green")
    for path in saves:
      path = path.rsplit( ".", 1 )[ 0 ] #usuwa json
      print(str(number) + ". ", end="")
      Konsola.print(path, "lwhite")
      number+=1
    print("")
    
    correct = False
    while not correct:
      Konsola.print("Wybierz zapis: ", "lgreen", line_end='')
      choice = input()
      try:
        choice = int(choice)
      except:
        if choice == "q":
          return
        print("Podaj liczbę ")
        continue
      if 0 < choice <= len(saves):
        self.load_game(saves[choice-1])
        return
      else:
        print("Nie ma takiego zapisu ")