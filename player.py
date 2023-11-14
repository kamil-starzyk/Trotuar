from konsola import Konsola
from helper import Helper
from mob import Mob
from item import Item

class Player(Mob):
  def __init__(self, x, y, z, name, alias, description, lvl, exp, weight, money, race, proficiency, params, stats, equipment, slots, conversations, knowledge):
    super(Player, self).__init__(x, y, z, name, alias, description, lvl, exp, weight, money, race, proficiency, params, stats, equipment, slots, conversations, knowledge)
    self.quest_id = None
    self.picked_item = None
    self.droped_item = None
    self.given_item = None
    self.item_receiver = None
    self.mob_killed= None

  def whoami(self):
    print("Jestem " + self.name + ", rasa: " + self.race + "\n" + self.description)
    print("Poziom: " + str(self.lvl) + " ( " + str(self.exp) + " / " + str(self.max_exp_for_level(self.lvl)) + " )")

  def whereami(self):
    print("Znajduję się w "+self.current_location.name + ". Moje współrzędne to:")
    print('"x": ' + str(self.x)+',')
    print('"y": ' + str(self.y)+',')
    print('"z": ' + str(self.z))
  
  def max_exp_for_level(self, level):
    if level == 1:
      return 30
    else:
      return self.max_exp_for_level(level - 1) + 10 * (level - 1)
    
  def add_exp(self, exp):
    self.exp += exp
    while self.exp >= self.max_exp_for_level(self.lvl):
      self.lvl += 1
      Konsola.print(" >> Gratulacje! Osiągnąłeś kolejny poziom główny ( " + str(self.lvl) + " ) <<", "lgreen")
      self.exp -= self.max_exp_for_level(self.lvl-1)

  def move_in_direction(self, direction):
    if super().move_in_direction(direction):
      self.my_square().show_square()
    else: print("Nie możesz tam przejść")
  
  def pick_up(self, item_name):
    item = super().pick_up(item_name)
    if item:
      self.picked_item = item
      Konsola.print("Podniosłeś ", line_end='')
      Konsola.print(item.name, "lwhite")
    else:
      Konsola.print("Nie ma tu takiej rzeczy", "red")
  
  def drop(self, item_name):
    item = super().drop(item_name)
    if item:
      self.droped_item = item
      Konsola.print("Upuściłeś ", line_end='')
      Konsola.print(item.name, "lwhite")
    else:
      Konsola.print("Nie masz takiej rzeczy w ekwipunku", "red")
  
  def give(self, item_name):
    item = Helper.find_item(self.equipment, item_name)
    if item:
      mobs = self.current_location.mobs_on_square(self.my_square())
      mob = None
      if len(mobs) == 1:
        mob = mobs[0]
      else:
        Konsola.print("Komu chcesz przekazać " + item.name +"?", "lcyan", line_end=' ')
        mob_name = input()
        mob = Helper.find_item(mobs, mob_name)
      if mob:
        if item.stackable() and item.amount > 1:
          print("Jaką ilość chcesz podarować? (max: " + str(item.amount) + ")")
          amount_to_give = Konsola.int_input(1, item.amount)
          if amount_to_give == item.amount:
            self.equipment.remove(item)
          else:
            item = Item.unstack(item, amount_to_give)
        else:
          self.equipment.remove(item)

        mob.equipment.append(item)
        self.item_receiver = mob
        self.given_item = item
        return item
      else:
        Konsola.print("Nie udało się przekazać przedmiotu", "red")

  def see(self, item_name):
    item = Helper.find_item(self.equipment, item_name)
    if item:
      item.see_more()
      return 1
    item = Helper.find_item(self.my_square().items, item_name)
    if item:
      item.see_more()
      return 1
    mobs = self.current_location.mobs_on_square(self.my_square())
    mob = Helper.find_item(mobs, item_name)
    if mob: 
      mob.see_more()
      return 1
    Konsola.print("Nie ma tu takiej rzeczy, ani nie masz jej w ekwipunku. Nie ma tu także takiej osoby.", "red")
  
  def equip(self, item_name):
    item = super().equip(item_name)
    if item:
      print("Założyłeś " + item.name)
    else:
      Konsola.print("Nie masz takiej rzeczy w ekwipunku", "red")
  
  def unequip(self, item_name):
    item = super().unequip(item_name)
    if item:
      print("Zdjąłeś " + item.name)
    else:
      Konsola.print("Nie masz takiej rzeczy na sobie", "red")
  
  def outfit(self):
    Konsola.print("Twoje wyposarzenie", "lcyan")
    super().outfit()


  def navigate_conversation(self, current_step):
    options = []
    for option in current_step.get("options", []):
      condition = option.get("condition")
      if condition is None or self.knowledge.get(condition, False):
        options.append(option)

    if not options:
      return
    
    number = 1
    for option in options:
      Konsola.print(" (" + str(number) + ".) " + option["text"])
      number+=1
      
    choice = Konsola.int_input()
    if 1 <= choice <= len(options):
      selected_option = options[choice - 1]
      Konsola.wrap(selected_option["response"], "lwhite")
      if selected_option.get("knowledge"):
        for key, value in selected_option["knowledge"].items():
          if key not in self.knowledge:
            self.knowledge[key] = value
      if selected_option.get("forget"):
        key = selected_option.get("forget")
        if key in self.knowledge:
          del self.knowledge[key]
          
      if "quest_id" in selected_option:
        quest_id = selected_option["quest_id"]
        self.quest_id = quest_id
      Helper.sleep(1)
      next_step = selected_option.get("next_step")
      if next_step:
        self.navigate_conversation(next_step)
      elif choice == len(options):
        return
      else:
        self.navigate_conversation(current_step)
    else:
      print("Błędny wybór")
      self.navigate_conversation(current_step)

  def talk_to(self, mob_name):
    mobs = self.current_location.mobs_on_square(self.my_square())
    mob = Helper.find_item(mobs, mob_name)
    if mob: 
      if mob.conversations:
        Konsola.print(mob.conversations["greeting"], "lwhite")
        self.navigate_conversation(mob.conversations)
      else:
        print(mob.name + " nie ma Ci nic do powiedzenia")

  def compare(self, mob_name):
    mobs = self.current_location.mobs_on_square(self.my_square())
    mob = Helper.find_item(mobs, mob_name)
    if mob: 
      Konsola.print("Porównujesz się z " + mob.name, "lwhite")
      Konsola.hr()

      mob_offensive_score = 0
      mob_offensive_score += mob.stats["attack"]
      mob_offensive_score += mob.stats["strength"]
      mob_offensive_score += mob.stats["speed"]/3
      mob_offensive_score += mob.stats["dexterity"]/2

      my_offensive_score = 0
      my_offensive_score += self.stats["attack"]
      my_offensive_score += self.stats["strength"]
      my_offensive_score += self.stats["speed"]/3
      my_offensive_score += self.stats["dexterity"]/2

      mob_defensive_score = 0
      mob_defensive_score += mob.stats["defence"]
      mob_defensive_score += mob.stats["speed"]
      mob_defensive_score += mob.stats["dexterity"]/2

      my_defensive_score = 0
      my_defensive_score += self.stats["defence"]
      my_defensive_score += self.stats["speed"]
      my_defensive_score += self.stats["dexterity"]/2

      off_result = mob_offensive_score / my_offensive_score
      # print(f"(Atak) {mob.name}: {mob_offensive_score}")
      # print(f"(Atak) {self.name}: {my_offensive_score}")
      if off_result < 0.8:
        Konsola.print("Twój przeciwnik jest słabszy od Ciebie w ataku", "green")
      elif 0.8 <= off_result < 1.2 :
        Konsola.print("Twój przeciwnik jest porównywalny do Ciebie w ataku", "yellow")
      else:
        Konsola.print("Twój przeciwnik jest silniejszy od Ciebie w ataku", "red")

      def_result = mob_defensive_score / my_defensive_score
      # print(f"(Obrona) {mob.name}: {mob_defensive_score}")
      # print(f"(Obrona) {self.name}: {my_defensive_score}")
      if def_result < 0.8:
        Konsola.print("Twój przeciwnik jest słabszy od Ciebie w obronie", "green")
      elif 0.8 <= def_result < 1.2 :
        Konsola.print("Twój przeciwnik jest porównywalny do Ciebie w obronie", "yellow")
      else:
        Konsola.print("Twój przeciwnik jest silniejszy od Ciebie w obronie", "red")
      
      if mob.hp/mob.hp_max < 0.5:
        Konsola.print("Przeciwnik nie wydaje się czuć zbyt dobrze", "lred")
      elif 0.5 <= mob.hp/mob.hp_max < 0.8:
        Konsola.print("Wygląda na to, że przeciwnik w dobrym stanie", "lblue")
      else:
        Konsola.print("Przeciwnik wygląda jakby czuł się doskonale", "lgreen")

  def kill(self, mob_name):
    if self.stamina <= 10:
      print("Nie masz siły walczyć")
      return
    
    mobs = self.current_location.mobs_on_square(self.my_square())
    mob = Helper.find_item(mobs, mob_name)

    if not mob:
      Konsola.print("Nie ma tu kogoś takiego", "red")
      return

    def player_and_mob_params():
      Konsola.print_param("Ja", self.hp, self.hp_max, "lred")
      Konsola.print_param("stamina", self.stamina, self.stamina_max, "lyellow")
      print("")
      Konsola.print_param(mob.name, mob.hp, mob.hp_max, "red")
      Konsola.print_param("stamina", mob.stamina, mob.stamina_max, "yellow")
    
    def award_exp(fraction=1):
      Konsola.print("  Zdobywasz: ", line_end="")
      exp = int(mob.exp*fraction)
      Konsola.print(str(exp) + " doświadczenia", "lyellow")
      self.add_exp(exp)
      mob.exp-=exp
    
    def award_money():
      Konsola.print("  Zdobywasz: ", line_end="")
      Konsola.print(str(mob.money) + " złota", "lyellow")
      self.money+=mob.money
      mob.money = 0
    
    mob.try_to_draw_weapon()
    print("Walczysz z " + mob.name)
    while self.hp > self.hp_max/10 and mob.hp > mob.hp_max/10:
      player_and_mob_params()
      if self.stamina <= 11:
        Konsola.print("Odpocznij!!!", "lred")
        self.adjust_stamina(5, 0.5)
      else:
        damage_given = self.hit(mob)
        if damage_given:
          mob.hp -= damage_given
          Konsola.damage_given(True, mob, damage_given)
          mob.adjust_stamina(-damage_given/2, -damage_given/4)
        else:
          print("Chybiłeś")
          if mob.hp <= mob.hp_max/2:
            direction = mob.try_to_escape()
            if direction:
              print(mob.name + " uciekł " + Konsola.direction_translator(direction))
              return
        self.adjust_stamina(-5, -1)

      if mob.hp > mob.hp_max/10:
        if mob.stamina <= 11:
          Konsola.print("Przeciwnik czeka", "red")
          mob.adjust_stamina(5, 0.5)
        else:
          damage_taken = mob.hit(self)
          if damage_taken:
            self.hp -= damage_taken
            Konsola.damage_given(False, mob, damage_taken)
            self.adjust_stamina(-damage_given/2, -damage_given/4)
          else:
            print(f'{mob.name} chybia')
          mob.adjust_stamina(-5, -1)
      Helper.sleep(1)
      Konsola.clear()

    if 0 < mob.hp < mob.hp_max/5 and self.hp > self.hp_max/5:
      Konsola.print("Twój przeciwnik chwieje się na nogach i nie jest w stanie walczyć. Co robisz?", "cyan")
      print("[1] Dobij go!")      
      print("[2] Daruj życie i pozwól odejść")      
      print("[3] Pozwól odejść, ale ma oddać wszystkie pieniądze")
      choice = Konsola.int_input(1,3)
      if choice == 1:
        damage_given = mob.hp
        mob.hp-=damage_given
        Konsola.damage_given(True, mob, damage_given)
      elif choice == 3:
        if mob.money > 0:
          award_money()
        if mob.exp > 0:
          award_exp(0.5)
        direction = mob.try_to_escape()
        Konsola.print("Przeciwnik uciekł" + Konsola.direction_translator(direction), "cyan")
        return
      else:
        if mob.exp > 0:
          award_exp(0.75)
        mob.try_to_escape(100)
        Konsola.print("Przeciwnik uciekł dziękując za łaskę", "cyan")
        return

    elif 0 < self.hp < self.hp_max/5 and mob.hp > mob.hp_max/5:
      Konsola.print("Jesteś zbyt pobity by walczyć", "cyan")
      wants_to_kill_you = Helper.random()
      if wants_to_kill_you > 60:
        Konsola.print("Przeciwnik postanowił Cię wykończyć", "cyan")
        damage_taken = self.hp
        self.hp-=damage_taken
        Konsola.damage_given(False, mob, damage_taken)
      else:
        Konsola.print("Przeciwnik daruje Ci życie", "cyan")
    

    if self.hp > 0 and mob.hp == 0:
      Konsola.print("Pokonałeś " + mob.name, "lgreen")
      if mob.money > 0:
        award_money()
      if mob.exp > 0:
        award_exp()
      mob.die()
        
    elif self.hp == 0 and mob.hp > 0:
      Konsola.print("Zostałeś pokonany przez " + mob.name, "lred")
    
    else:
      Konsola.print("Obaj jesteście u kresu życia, żaden nie jest w stanie rozstrzygnąć walki.", "cyan")
      award_exp(0.5)
        

  def rest(self, how_long=""):
    resting_stories = [
      "Patrzysz na przelatujące obłoczki",
      "Drapiesz się po tyłku",
      "Grzebiesz sobie w uchu",
      "Słuchasz co w trawie piszczy",
      "Wstajesz, przeciągasz się i siadasz z powrotem na kamieniu",
      "Robisz pajacyki",
      "Rozdzielasz źdźbło trawy na czworo",
      "Zastanawiasz się nad sensem zycia",
      "Ziewasz głośno",
      "Nucisz rubaszną piosenkę",
      "Liczysz mrówki chodzące Ci po nodze",
      "Obserwujesz spadające liście i udajesz, że to sztorm meteorów",
      "Odliczasz oddechy ślimaka, który przechodzi obok",
      "Organizujesz zawody w skakaniu kamykiem po kałuży",
      "Zbierasz niewidzialne kamyki i układasz je w piramidę",
      "Ćwiczysz siedemnastotomową sztuczkę językową",
      "Próbujesz złapać wiatr w swoje dłonie",
      "Symulujesz rozmowę ze zmyślonym przyjacielem",
      "Rozmawiasz z drzewem i udajesz, że zrozumiało twoje pytanie",
      "Organizujesz wyścigi mrówek, przyznając medal za zwycięstwo",
      "Zapraszasz mrówki na herbatę i dyskutujesz z nimi o polityce mrówkowej"
    ]

    start_hp = self.hp
    start_stamina = self.stamina
    try:
      how_long = int(how_long)
      for i in range(how_long):
        self.hp += 3
        self.adjust_stamina(15, 2)
        Konsola.print_random(resting_stories)
        print("")
        Konsola.print_param("HP", self.hp, self.hp_max, "lred")
        Konsola.print_param("Stamina", self.stamina, self.stamina_max, "lyellow")
        print("")
        Helper.sleep(1)
    except ValueError:
      print("Musisz podać ilość godzin jaką chcesz odpoczywać.") 
      return 0
      
    end_hp = self.hp
    end_stamina = self.stamina
    Helper.sleep(1)
    Konsola.print("Odpoczywałeś przez " + str(how_long) + " godzin", "green")
    Konsola.print("Podczas odpoczynku odzyskałeś " + str(int(end_hp - start_hp)) + " zdrowia", "lgreen")
    Konsola.print("oraz odpocząłeś o " + str(int(end_stamina - start_stamina)) + " punktów staminy", "lyellow")
    return how_long*3600

  def sleep(self, how_long=""):
    bed = Helper.find_utility("sleep")
    if not bed:
      Konsola.print("Tu nie ma na czym spać", "red")
      return 0

    start_hp = self.hp
    start_stamina = self.stamina
    comfort_factor = bed.attr["comfort"]/100
    try:
      how_long = int(how_long)
      for i in range(how_long):
        self.hp += 16 * comfort_factor
        self.adjust_stamina(24*comfort_factor, 16*comfort_factor)
        Konsola.print_param("HP", self.hp, self.hp_max, "lred")
        Konsola.print_param("Stamina", self.stamina, self.stamina_max, "lyellow")
        print("")
        Helper.sleep(1)
    except ValueError:
      print("Musisz podać ilość godzin jaką chcesz spać") 
      return 0  

    end_hp = self.hp
    end_stamina = self.stamina
    Helper.sleep(1)
    Konsola.print("Spałeś " + str(how_long) + " godzin", "green")
    Konsola.print("Podczas snu odzyskałeś " + str(int(end_hp - start_hp)) + " zdrowia", "lgreen")
    Konsola.print("oraz odpocząłeś o " + str(int(end_stamina - start_stamina)) + " punktów staminy", "lyellow")

    return how_long*3600

  def use_passage(self, direction):
    passages = self.current_location.secret_passages
    for p in passages:
      if p["x"] == self.x and p["y"] == self.y and p["z"] == self.z:
        if p["direction"] == direction and p["condition"] in self.knowledge:
          match direction:
            case "n":
              self.y -= 1
            case "e":
              self.x += 1
            case "s":
              self.y += 1
            case "w":
              self.x -= 1
            case "u":
              self.z += 1
            case "d":
              self.z -= 1
          print("Skorzystałeś z tajnego przejścia")
          Helper.sleep(1)
          self.my_square().show_square()
          return
    print("Chyba nie tędy droga...")
      

  def to_dict(self):
    player = super().to_dict()
    return player
  
  @classmethod
  def from_dict(cls, data):
    eq = [Item.from_dict(item_data) for item_data in data["equipment"]]
    slots = data["slots"]
    for key in slots:
      if slots[key] == {}:
        slots[key] = None
      else:
        slots[key] = Item.from_dict(slots[key])
    
    return cls(data["x"], data["y"], data["z"], data["name"], data["alias"], data["description"], data["lvl"], data["exp"], data["weight"], data["money"],data["race"], data["proficiency"], data["params"], data["stats"], eq, slots, data["conversations"], data["knowledge"])