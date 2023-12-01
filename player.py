from random import shuffle
from konsola import Konsola
from helper import Helper
from mob import Mob
from item import Item

class Player(Mob):
  TIME_OF_MOVEMENT = 60
  TIME_OF_ITEM_INTERACTION = 30
  TIME_OF_CONVERSATION = 90
  TIME_OF_EXCHANGING_BLOWS = 30
  def __init__(self, mob_id, x, y, z, base_name, name, alias, description, lvl, exp, weight, money, race, proficiency, params, stats, equipment, slots, conversations, knowledge, path, killable, can_duel, is_aggressive, can_ally, affiliation):
    super(Player, self).__init__(mob_id, x, y, z, base_name, name, alias, description, lvl, exp, weight, money, race, proficiency, params, stats, equipment, slots, conversations, knowledge, killable, path, can_duel, is_aggressive, can_ally, affiliation)
    self.game = None
    self.quest_id = None
    self.picked_item = None
    self.droped_item = None
    self.given_item = None
    self.item_receiver = None
    self.talk_to_npc = None
    self.mobs_killed = []

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
      return self.max_exp_for_level(level - 1) + 10 * (level+2)
    
  def add_exp(self, exp):
    exp = int(exp)
    self.exp += exp
    while self.exp >= self.max_exp_for_level(self.lvl):
      self.lvl += 1
      Konsola.print(" >> Gratulacje! Osiągnąłeś kolejny poziom główny ( " + str(self.lvl) + " ) <<", "lgreen")
      self.exp -= self.max_exp_for_level(self.lvl-1)

  def move_in_direction(self, direction):
    if super().move_in_direction(direction):
      self.my_square.show_square()
      return Player.TIME_OF_MOVEMENT/self.stat_coefficient(self.speed)

    print("Nie możesz tam przejść")
    return 0

  
  def pick_up(self, item_name):
    item = super().pick_up(item_name, True)
    if item:
      self.picked_item = item
      Konsola.print("Podniosłeś ", line_end='')
      Konsola.print(item.name, "lwhite")
      return Player.TIME_OF_ITEM_INTERACTION

    Konsola.print("Nie ma tu takiej rzeczy", "red")
    return 0
  
  def drop(self, item_name):
    item = super().drop(item_name, True)
    if item:
      self.droped_item = item
      Konsola.print("Upuściłeś ", line_end='')
      Konsola.print(item.name, "lwhite")
      return Player.TIME_OF_ITEM_INTERACTION
    
    Konsola.print("Nie masz takiej rzeczy w ekwipunku", "red")
    return 0

  def use(self, item_name):
    item, effects = super().use(item_name, True)
    if effects:
      Konsola.print("Zużyłeś ", line_end='')
      Konsola.print(item.name, "lwhite")
      print("Efekty: ")
      for e in effects:
        print(e + ": +" +str(effects[e]))
  
  def give(self, item_name):
    item = Helper.find_item(self.equipment, item_name, True)
    if not item:
      Konsola.print("Nie masz takiej rzeczy w ekwipunku", "red")
      return 0

    mobs = self.current_location.mobs_on_square(self.my_square)
    mob = None
    if len(mobs) == 1:
      mob = mobs[0]
    else:
      Konsola.print("Komu chcesz przekazać " + item.name +"?", "lcyan", line_end=' ')
      mob_name = input()
      mob = Helper.find_item(mobs, mob_name, True)

    if not mob:
      Konsola.print("Nie udało się przekazać przedmiotu", "red")
      return 0

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
    return Player.TIME_OF_ITEM_INTERACTION
    
    
    

  def see(self, item_name):
    item = Helper.find_item(self.equipment, item_name, True)
    if item:
      item.see_more()
      return 1
    item = Helper.find_item(self.my_square.items, item_name, True)
    if item:
      item.see_more()
      return 1
    utility = Helper.find_item(self.my_square.utilities, item_name, True)
    if utility:
      utility.see_more()
      return 1
    mobs = self.current_location.mobs_on_square(self.my_square)
    mob = Helper.find_item(mobs, item_name, True)
    if mob: 
      mob.see_more()
      return 1
    Konsola.print("Nie ma tu takiej rzeczy, ani nie masz jej w ekwipunku. Nie ma tu także takiej osoby.", "red")
  
  def search_utility(self, item_name):
    utility = Helper.find_item(self.my_square.utilities, item_name, True)
    if utility:
      utility.show_items()
      return 1
    Konsola.print("Nie ma tu takiej rzeczy.", "red")

  def equip(self, item_name):
    item = super().equip(item_name, True)
    if item:
      print("Założyłeś " + item.name)
      return Player.TIME_OF_ITEM_INTERACTION
      #TODO zmiana na tym samym slocie
    
    Konsola.print("Nie masz takiej rzeczy w ekwipunku", "red")
    return 0
  
  def unequip(self, item_name):
    item = super().unequip(item_name, True)
    if item:
      print("Zdjąłeś " + item.name)
      return Player.TIME_OF_ITEM_INTERACTION
    
    Konsola.print("Nie masz takiej rzeczy na sobie", "red")
    return 0
  
  def outfit(self):
    Konsola.print("Twoje wyposarzenie", "lcyan")
    super().outfit()
    return 0


  def navigate_conversation(self, current_step, total_time=0):
    options = []
    for option in current_step.get("options", []):
      condition = option.get("condition")
      if condition is None or self.knowledge.get(condition, False):
        options.append(option)

    if not options:
      return total_time
    
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
        total_time += self.navigate_conversation(next_step)
      elif choice == len(options):
        return total_time
      else:
        self.navigate_conversation(current_step)
    else:
      print("Błędny wybór")
      self.navigate_conversation(current_step)
    
    return total_time + Player.TIME_OF_CONVERSATION


  def talk_to(self, mob_name):
    mobs = self.current_location.mobs_on_square(self.my_square)
    mob = Helper.find_item(mobs, mob_name, True)
    if mob: 
      if mob.conversations:
        Konsola.print(mob.conversations["greeting"], "lwhite")
        conv_time = self.navigate_conversation(mob.conversations)
        return conv_time
      print(mob.name + " nie ma Ci nic do powiedzenia")
      return 0
    Konsola.print("Nie ma tu kogoś takiego", "red")
    return 0
    

  def compare(self, mob_name):
    mobs = self.current_location.mobs_on_square(self.my_square)
    mob = Helper.find_item(mobs, mob_name, True)
    if mob: 
      Konsola.print("Porównujesz się z " + mob.name, "lwhite")
      Konsola.hr()

      def calculate_offensive_score(mob):
        offensive_score = 0
        offensive_score += mob.stats["attack"]
        offensive_score += mob.stats["strength"]
        offensive_score += mob.stats["speed"]/3
        offensive_score += mob.stats["dexterity"]/2
        return offensive_score

      def calculate_defensive_score(mob):
        defensive_score = 0
        defensive_score += mob.stats["defence"]
        defensive_score += mob.stats["speed"]
        defensive_score += mob.stats["dexterity"]/2
        return defensive_score

      mob_offensive_score = calculate_offensive_score(mob)
      my_offensive_score = calculate_offensive_score(self)
      mob_defensive_score = calculate_defensive_score(mob)
      my_defensive_score = calculate_defensive_score(self)

      off_result = mob_offensive_score / my_offensive_score
      if off_result < 0.8:
        Konsola.print("Twój przeciwnik jest słabszy od Ciebie w ataku", "green")
      elif 0.8 <= off_result < 1.2 :
        Konsola.print("Twój przeciwnik jest porównywalny do Ciebie w ataku", "yellow")
      else:
        Konsola.print("Twój przeciwnik jest silniejszy od Ciebie w ataku", "red")

      def_result = mob_defensive_score / my_defensive_score
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
      return 0
    
    mobs = self.current_location.mobs_on_square(self.my_square)
    mob = Helper.find_item(mobs, mob_name, True)

    if not mob:
      Konsola.print("Nie ma tu kogoś takiego", "red")
      return 0

    enemies = []
    enemies.append(mob)
    current_enemy_index = 0

    def player_and_mob_params():
      Konsola.clear()
      Konsola.print_param("Ja", self.hp, self.hp_max, "lred")
      Konsola.print_param("stamina", self.stamina, self.stamina_max, "lyellow")
      Konsola.print_param("mana", self.mana, self.mana_max, "lblue")
      for mob in enemies:
        if mob.hp > 0:
          print("")
          Konsola.print_param(mob.name, mob.hp, mob.hp_max, "red")
          Konsola.print_param("stamina", mob.stamina, mob.stamina_max, "yellow")
    
    def award_exp(mob, fraction=1):
      Konsola.print("  Zdobywasz: ", line_end="")
      exp = int(mob.exp*fraction)
      Konsola.print(str(exp) + " doświadczenia", "lyellow")
      self.add_exp(exp)
      mob.exp-=exp
    
    def award_money(mob):
      Konsola.print("  Zdobywasz: ", line_end="")
      Konsola.print(str(mob.money) + " złota", "lyellow")
      self.money+=mob.money
      mob.money = 0
    
    def check_for_more_enemies():
      if len(enemies) > 0:
        mobs = self.current_location.mobs_on_square(self.my_square)
        rats = [mob for mob in mobs if mob.base_name == "Szczur"]
        for rat in rats:
          if rat not in enemies and any(affiliation in rat.affiliation for affiliation in enemies[0].affiliation):
            enemies.append(rat)
            print('')
            Konsola.print(rat.name + " dołączył do walki", "lred")
            rat.try_to_draw_weapon()
            Helper.sleep(0.5)
            return
    
    player_resulting_speed = self.stat_coefficient(self.speed)

    mob.try_to_draw_weapon()
    print("Walczysz z " + mob.name)

    call_for_help = mob.call_for_help()
    if call_for_help:
      print(mob.name + " głośno zapiszczał")
      Helper.sleep(1)

    while self.hp > self.hp_max/10 and any(mob.hp > mob.hp_max/10 for mob in enemies):
      player_and_mob_params()
      if self.stamina <= 11:
        Konsola.print("Odpocznij!!!", "lred")
        self.adjust_stamina(5, 0.5)
      else:
        choice = Konsola.dynamic_prompt()

        
        if choice in ("next", "n"):
          current_enemy_index = (current_enemy_index + 1) % len(enemies)
          mob = enemies[current_enemy_index]
          Konsola.print("  Teraz atakujesz " + mob.name, "yellow")
          choice = Konsola.dynamic_prompt()
          
        elif choice in ("prev", "p"):
          current_enemy_index = (current_enemy_index - 1) % len(enemies)
          mob = enemies[current_enemy_index]
          Konsola.print("  Teraz atakujesz " + mob.name, "yellow")
          choice = Konsola.dynamic_prompt()
        
        if choice in ("/", "?"):
          combat_actions = {
            ("next", "n"): "Następny przeciwnik",
            ("prev", "p"): "Poprzedni przeciwnik",
            ("cios", "c"): "Prosty cios",
            ("zamach", "z"): "Szeroki zamach, próba trafienia kilku przeciwników",
            ("garda", "g"): "Czekaj",
          }
          for c in combat_actions:
            print(c , end=' - ')
            print(combat_actions[c])
          input("Kontynuuj walkę")

        elif choice in ("garda", "g"):
          Konsola.print("Czekasz", "lred")
          self.adjust_stamina(5, 0.5)
          self.chance_bonus += 15

        elif choice in ("zamach", "z"):
          enemies_hit, damage_sum = self.swing(enemies)
          if enemies_hit:
            Konsola.print(f'Wykonałeś skuteczny zamach! Trafiłeś {enemies_hit} przeciwników, zadając w sumie {damage_sum} obrażeń', "lwhite")
            self.chance_bonus = 0
          else:
            Konsola.print(f'Straciłeś równowagę próbując się zamachnąć')
            self.chance_bonus -= 5
            self.adjust_stamina(-5, -1)

        elif choice in ("cios", "c") or 1:
          damage_given = self.hit(mob)
          if damage_given:
            mob.hp -= damage_given
            Konsola.damage_given(True, mob, damage_given)
            mob.adjust_stamina(-damage_given/2, -damage_given/4)
            self.chance_bonus = 0
          else:
            print("Chybiłeś")
            self.chance_bonus += 8
            if mob.hp <= mob.hp_max/2:
              direction = mob.try_to_escape()
              if direction:
                Konsola.print("  " + mob.name + " uciekł " + Konsola.direction_translator(direction), "cyan")
                Helper.sleep(0.5)
                enemies.remove(mob)
            self.adjust_stamina(-5, -1)

        
        time_of_action = Player.TIME_OF_EXCHANGING_BLOWS/self.stat_coefficient(self.speed)
        self.game.update_state(time_of_action)
        Helper.sleep(0.5)

      enemies_actions = []
      if enemies:
        for i in range(len(enemies)):
          mob = enemies[i]
          if mob.hp > mob.hp_max/10:
            if mob.stamina <= 11:
              Konsola.print(mob.name + " czeka", "red")
              mob.adjust_stamina(5, 0.5)
            else:
              mob_resulting_speed = self.stat_coefficient(mob.speed)
              speed_advantage = mob_resulting_speed / player_resulting_speed
              mob_hits = Helper.probabilistic_round(speed_advantage)
              for _ in range(mob_hits):
                action = []
                action.append(mob)
                action.append(mob.hit)
                enemies_actions.append(action)
              

          elif 0 < mob.hp <= mob.hp_max/10 and len(enemies)>1:
            direction = mob.try_to_escape(100)
            if direction:
              Konsola.print("  " + mob.name + " uciekł " + Konsola.direction_translator(direction), "cyan")
              Helper.sleep(0.5)
              enemies.remove(mob)

      shuffle(enemies_actions)
      for a in enemies_actions:
        mob = a[0]
        action = a[1]
        damage_taken = action(self)
        if damage_taken:
          self.hp -= damage_taken
          Konsola.damage_given(False, mob, damage_taken)
          self.adjust_stamina(-damage_taken/2, -damage_taken/4)
        else:
          print(f'{mob.name} chybia')
          mob.adjust_stamina(-5, -1)
        time_of_action = Player.TIME_OF_EXCHANGING_BLOWS/self.stat_coefficient(mob.speed)
        self.game.time.time_progress(time_of_action)
        Helper.sleep(0.5)
      
      check_for_more_enemies()

      Helper.sleep(0.5)

    if 0 < mob.hp < mob.hp_max/10 and self.hp > self.hp_max/10:
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
          award_money(mob)
        if mob.exp > 0:
          award_exp(mob, 0.5)
        direction = mob.try_to_escape(100)
        Konsola.print("Przeciwnik uciekł" + Konsola.direction_translator(direction), "cyan")
        return 0
      else:
        if mob.exp > 0:
          award_exp(mob, 0.75)
        mob.try_to_escape(100)
        Konsola.print("Przeciwnik uciekł dziękując za łaskę", "cyan")
        return 0

    elif 0 < self.hp < self.hp_max/10 and mob.hp > mob.hp_max/10:
      Konsola.print("Jesteś zbyt pobity by walczyć", "cyan")
      wants_to_kill_you = Helper.random()
      if wants_to_kill_you > 60:
        Konsola.print("Przeciwnik postanowił Cię wykończyć", "cyan")
        damage_taken = self.hp
        self.hp-=damage_taken
        Konsola.damage_given(False, mob, damage_taken)
      else:
        Konsola.print("Przeciwnik daruje Ci życie", "cyan")
    
    if self.hp > 0:
      for mob in enemies:
        if mob.hp == 0:
          Konsola.print("Pokonałeś " + mob.name, "lgreen")
          if mob.money > 0:
            award_money(mob)
          if mob.exp > 0:
            award_exp(mob)
          mob.die()
          self.mobs_killed.append(mob)
        
    elif self.hp == 0 and mob.hp > 0:
      Konsola.print("Zostałeś pokonany przez " + mob.name, "lred")
    
    else:
      Konsola.print("Nie jesteście w stanie rozstrzygnąć walki.", "cyan")
      award_exp(mob, 0.5)
    
    
    return 0
        

  def rest(self, hours=""):
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
      hours = int(hours)
      for i in range(hours):
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
    Konsola.print("Odpoczywałeś przez " + str(hours) + " godzin", "green")
    Konsola.print("Podczas odpoczynku odzyskałeś " + str(int(end_hp - start_hp)) + " zdrowia", "lgreen")
    Konsola.print("oraz odpocząłeś o " + str(int(end_stamina - start_stamina)) + " punktów staminy", "lyellow")
    return hours*3600

  def sleep(self, hours=""):
    bed = Helper.find_utility(self.my_square.utilities, "sleep")
    if not bed:
      Konsola.print("Tu nie ma na czym spać", "red")
      return 0

    start_hp = self.hp
    start_stamina = self.stamina
    comfort_factor = bed.attr["comfort"]/100
    try:
      hours = int(hours)
      for i in range(hours):
        self.hp += 10 * comfort_factor
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
    Konsola.print("Spałeś " + str(hours) + " godzin", "green")
    Konsola.print("Podczas snu odzyskałeś " + str(int(end_hp - start_hp)) + " zdrowia", "lgreen")
    Konsola.print("oraz odpocząłeś o " + str(int(end_stamina - start_stamina)) + " punktów staminy", "lyellow")

    return hours*3600

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
          self.my_square.show_square()
          return Player.TIME_OF_MOVEMENT/self.stat_coefficient(self.speed)
    print("Chyba nie tędy droga...")
    return 0
      

  def to_dict(self):
    player = super().to_dict()
    return player
  
  @classmethod
  def from_dict(cls, data):
    mob_id = data["mob_id"]
    if mob_id in Mob.ids:
      raise ValueError(f"Duplicate mob ID found: {mob_id}")
    cls.ids[mob_id] = data["name"]
    eq = [Item.from_dict(item_data) for item_data in data["equipment"]]
    slots = data["slots"]
    for key in slots:
      if slots[key] == {}:
        slots[key] = None
      else:
        slots[key] = Item.from_dict(slots[key])
    
    return cls(data["mob_id"], data["x"], data["y"], data["z"], data["base_name"], data["name"], data["alias"], data["description"], data["lvl"], data["exp"], data["weight"], data["money"],data["race"], data["proficiency"], data["params"], data["stats"], eq, slots, data["conversations"], data["knowledge"], data["killable"], data["path"], data["can_duel"], data["is_aggressive"], data["can_ally"], data["affiliation"])