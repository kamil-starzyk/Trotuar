from random import shuffle
from konsola import Konsola
from helper import Helper
from mob import Mob
from item import Item
from activity import Activity
from blueprint import Blueprint
from equipment import Equipment
from combat import Combat

class Player(Mob):
  TIME_OF_MOVEMENT = 60
  TIME_OF_ITEM_INTERACTION = 30
  TIME_OF_CONVERSATION = 90
  TIME_OF_EXCHANGING_BLOWS = 30

  def __init__(self, mob_id, x, y, z, base_name, name, alias, description, lvl, exp, weight, money, race, proficiency, params, stats, skills, equipment, slots, knowledge, journal, killable, can_duel, blueprints, affiliation):
    Mob.ids = {} #resets class property when game is reloaded
    super(Player, self).__init__(mob_id, x, y, z, base_name, name, alias, description, lvl, exp, weight, money, race, proficiency, params, stats, skills, equipment, slots, knowledge, journal, killable, can_duel, blueprints, affiliation)
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
    print("Mam " + str(self.money) + " pieniędzy")

  def whereami(self):
    print("Znajduję się w "+self.current_location.name + ". Moje współrzędne to:")
    print('"x": ' + str(self.x)+',')
    print('"y": ' + str(self.y)+',')
    print('"z": ' + str(self.z))
  
  def show_skills(self):
    for skill_group, skill_list in self.ALL_SKILLS.items():
      skill_group = skill_group.upper()
      Konsola.print(skill_group, "lwhite")
      for skill in skill_list:
        value = 0
        if skill in self.skills:
          value = self.skills[skill]
        Konsola.print(" - " + skill + ": ", line_end='')
        Konsola.print(value, "yellow")
  
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
    if item == 1:
      Konsola.print("Niesiesz zbyt duży ciężar albo ta rzecz waży za dużo", "red")
      return 0
    if item:
      self.picked_item = item
      Konsola.print("Podniosłeś ", line_end='')
      Konsola.print(item.name, "lwhite")
      if self.overloaded:
        Konsola.print("Jesteś przeciążony", "red")
      return Player.TIME_OF_ITEM_INTERACTION

    Konsola.print("Nie ma tu takiej rzeczy", "red")
    return 0

  def take(self, item_name):
    item = super().take(item_name, True)
    if item == 1:
      Konsola.print("Niesiesz zbyt duży ciężar albo ta rzecz waży za dużo", "red")
      return 0
    if item:
      self.picked_item = item
      Konsola.print("Wyjąłeś ", line_end='')
      Konsola.print(item.name, "lwhite")
      if self.overloaded:
        Konsola.print("Jesteś przeciążony", "red")
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
    amount_to_give = 1
    if item.stackable() and item.amount > 1:
      print("Jaką ilość chcesz podarować? (max: " + str(item.amount) + ")")
      amount_to_give = Konsola.int_input(1, item.amount)
    item = self.equipment.remove_item(item, amount_to_give)

    mob.equipment.add_item(item)
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
  
  def read(self, item_name):
    item = Helper.find_item(self.equipment, item_name, True)
    if item:
      time = item.read()
      return time
    item = Helper.find_item(self.my_square.items, item_name, True)
    if item:
      time = item.read()
      return time
    utility = Helper.find_item(self.my_square.utilities, item_name, True)
    if utility:
      time = utility.read()
      return time
    Konsola.print("Nie ma tu nio, co dałoby się przeczytać", "red")
  
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
    Konsola.print("Twoje wyposażenie", "lcyan")
    super().outfit()
    return 0

  def show_journal(self):
        if not self.journal:
            print("Journal is empty.")
            return

        # Iteruj przez główne kategorie w journalu
        for category, content in self.journal.items():
          print(f"\n{category.capitalize()}:")
            
          # Sprawdzaj, czy wartości w kategoriach to zagnieżdżone słowniki
          if isinstance(content, dict):
            for subcategory, subcontent in content.items():
              Konsola.print(f"  {subcategory.capitalize()}:", "lyellow")
                    
              # Sprawdzaj czy podkategorie mają dalsze zagnieżdżone słowniki
              if isinstance(subcontent, dict):
                for key, value in subcontent.items():
                  print(f"    {key}: {value}")
              else:
                print(f"    {subcontent}")
          else:
            print(f"  {content}")

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
      if selected_option.get("milestone"):
        #self.game.milestones.append(selected_option["milestone"])

        self.game.milestones[selected_option["milestone"]]["status"] = 1
            
      if selected_option.get("journal"):
        for journal_key, journal_value in selected_option["journal"].items():
          # Sprawdź, czy kategoria (np. "teachers") istnieje
          if journal_key not in self.journal:
            self.journal[journal_key] = journal_value
          else:
            # Jeśli kategoria istnieje, przetwarzaj jej podkategorie
            for sub_key, sub_value in journal_value.items():
              if sub_key not in self.journal[journal_key]:
                self.journal[journal_key][sub_key] = sub_value
              else:
                # Sprawdź jeszcze głębsze poziomy, jeśli są, np. "skills", "stats"
                for item_key, item_value in sub_value.items():
                  if item_key not in self.journal[journal_key][sub_key]:
                    self.journal[journal_key][sub_key][item_key] = item_value
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
  
  def trade(self, mob_name):
    mobs = self.current_location.mobs_on_square(self.my_square)
    mob = Helper.find_item(mobs, mob_name, True)
    if not mob: 
      Konsola.print("Nie ma tu kogoś takiego", "red")
      return 0
    if not mob.can_trade or len(mob.items_to_sell) == 0:
      Konsola.print(mob.name + " nie będzie z tobą handlować", "red")
      return 0
    def print_items(items):
      Konsola.clear()
      Konsola.print("Twoje pieniądze: ", line_end='')
      Konsola.print(self.money, "lyellow")
      Konsola.print("Przedmioty na sprzedaż: ", "yellow")
      Konsola.print_item_list(items)
      Konsola.print("Podaj numer przedmiotu lub jego nazwę aby zobaczyć szczegóły.", "yellow")
      Konsola.print("Aby nabyć przedmiot musisz napisać \"kup\" i nazwę przedmiotu albo jego numer", "lyellow")
      Konsola.print("Aby ponownie wyświetlić listę przedmiotów napisz \"lista\". Aby zakończyć handel napisz \"koniec\".", "yellow")
    
    time_of_trade = 30
    print_items(mob.items_to_sell)
    while True:
      is_buying = False
      Konsola.hr()
      choice = input(" > ")
      if choice == "lista":
        print_items(mob.items_to_sell)
        continue
      elif choice == "koniec":
        Konsola.print("Tylko się rozglądałem. Do zobaczenia.")
        break
      elif choice.startswith("kup "):
        choice = choice.replace("kup ", "", 1)
        is_buying = True

      try:
        item_index = int(choice) -1
      except ValueError:
        item_index = -1
      item = None
      if item_index >= 0 and item_index < len(mob.items_to_sell):
        item = mob.items_to_sell[item_index]
      elif item_index >= len(mob.items_to_sell):
        Konsola.print("Niewłaściwy numer", "red")
        continue
      else:
        item = Helper.find_item(mob.items_to_sell, choice, True)
      if item and not is_buying:
        item.see_more()
      elif item and is_buying:
        amount_to_buy = 1
        if item.stackable() and item.amount > 1:
          print("Jaką ilość chcesz kupić? (max: " + str(item.amount) + ")")
          amount_to_buy = Konsola.int_input(1, item.amount)
        price = item.price * amount_to_buy
        if self.money < price:
          Konsola.print("Nie stać Cię!", "red")
          continue

        if amount_to_buy < item.amount:
          unstacked_item = Item.unstack(item, amount_to_buy)
          self.equipment.add_item(unstacked_item) 
        else:
          mob.items_to_sell.remove(item)
          self.equipment.add_item(item)

        self.money -= price
        mob.money += price

        Konsola.print("Kupiłeś " + item.name + " za ", "lgreen", line_end='')
        Konsola.print(price, "lyellow")
        break
      else:
        Konsola.print("Nie ma takiego przedmiotu", "red")
      
      time_of_trade += 60
    return time_of_trade

  def train(self, trait):
    mobs = self.current_location.mobs_on_square(self.my_square)
    mob = None
    for m in mobs:
      if trait in m.teacher_of:
        mob = m
        break

    if not mob:
      Konsola.print("Nie ma tu nauczyciela, który mógłby Cię szkolić!", "lred")
      # return 0
    
    skills = []
    for v in self.ALL_SKILLS.values():
      skills += v

    if trait in self.stats:
      #Training of STAT  
      Konsola.print("To potrwa 2 godziny i będzie Cię kosztowało dużo wysiłku.", line_end=' ')
      Konsola.print(mob.name, "lwhite", line_end=' ')  
      Konsola.print("zażąda od Ciebie 10 pieniędzy za poświęcony czas")
      Konsola.print("Czy chcesz kontynuować? (Y/n)", 'lgreen')
      choice = input()
      if choice.lower() == "y":
        if self.stamina_max < 75:
          Konsola.print("Dziś jesteś już zbyt zmęczony na taki trening. Prześpij się i wróć jutro!", "lred")
          return 30
        if self.stamina < 75:
          Konsola.print("Odpocznij trochę zanim rozpoczniesz trening!", "lred")
          return 30
        if self.money < 10:
          Konsola.print("Nie stać Cię na zapłatę!", "lred")
          return 30
        Konsola.print(mob.name + " uczy Cię", line_end=' ')  
        Konsola.print(trait, "lwhite")
        self.money-= 10
        mob.money+= 10
        self.adjust_stamina(-70, -70)
        self.stats[trait] += 1
        Helper.sleep(1)
        Konsola.print("Jesteś bardzo zmęczony po treningu, ale zdobyłeś jeden punkt " + trait, "lyellow")
        return 7200
      else:
        print("Odchodzisz w pokoju")  
        return 30
    elif trait in skills:
    #Training of SKILL 
      Konsola.print("To potrwa 3 godziny i będzie Cię kosztowało trochę wysiłku.", line_end=' ')
      Konsola.print(mob.name, "lwhite", line_end=' ')  
      Konsola.print("zażąda od Ciebie 10 pieniędzy za poświęcony czas")
      Konsola.print("Czy chcesz kontynuować? (Y/n)", 'lgreen')
      choice = input()
      if choice.lower() == "y":
        if self.stamina_max < 50:
          Konsola.print("Dziś jesteś już zbyt zmęczony na taki trening. Prześpij się i wróć jutro!", "lred")
          return 30
        if self.stamina < 50:
          Konsola.print("Odpocznij trochę zanim rozpoczniesz trening!", "lred")
          return 30
        if self.money < 10:
          Konsola.print("Nie stać Cię na zapłatę!", "lred")
          return 30
        Konsola.print(mob.name + " uczy Cię", line_end=' ')  
        Konsola.print(trait, "lwhite")
        self.money-= 10
        mob.money+= 10
        self.adjust_stamina(-50, -50)
        if trait in self.skills:
          self.skills[trait] += 2
        else:
          self.skills[trait] = 2

        Helper.sleep(1)
        Konsola.print("Jesteś bardzo zmęczony po treningu, ale zdobyłeś jeden punkt " + trait, "lyellow")
        return 10800
      else:
        print("Odchodzisz w pokoju")  
        return 30
    else:
      Konsola.print("Próbowałeś się nauczyć czegoś co nie jest ani statystyką ani umiejętnością! Zaiste niebywałe, że widzisz tę wiadomość", "lred")

      

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
    enemy = Helper.find_item(mobs, mob_name, True)

    if not enemy:
      Konsola.print("Nie ma tu kogoś takiego", "red")
      return 0

    
    combat = Combat()
    self.game.combat = combat

    combat.add_combatant(enemy)
        

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
      
  def create(self, item_name):
    for blueprint in self.blueprints:
      if item_name not in blueprint.resulting_item["alias"]:
        Konsola.print("Nie masz odpowiedniego przepisu!", "lred")
        return 0
      
      print("Korzystasz z przepisu: ", end='')
      Konsola.print(blueprint.name, "lyellow")
      Konsola.hr()
      Konsola.wrap(blueprint.content)
      Konsola.hr()
      for skill, value in blueprint.skills_needed.items():
        try:
          self_skill_value = self.skills[skill]
        except KeyError:
          self_skill_value = 0
        if self_skill_value < value:
          
          Konsola.print("Twoja umiejętność: ", "lred", line_end='')
          Konsola.print(skill + " (" + str(self_skill_value) + ") ", 'lyellow', line_end='')
          Konsola.print("jest niewystarczająca! Potrzeba przynajmniej " + str(value) + ".", "lred")
          return 0
  
      tools_posesed = [] 
      for item in self.equipment:
        if "tool" in item.attr:
          tools_posesed.append(item.attr["tool"])
      
      missing_tools = [tool for tool in blueprint.tools_needed if tool not in tools_posesed]
      if missing_tools:
        Konsola.print("Nie posiadasz narzędzi: ", "lred", line_end='')
        Konsola.print(str(missing_tools), 'lyellow')
        Konsola.print("Potrzebne narzędzia: " + str(blueprint.tools_needed))
        return 0 
      
      materials_posesed = {} 
      for item in self.equipment:
        if "material" in item.attr:
          materials_posesed[item.attr["material"]] = item.amount
      
      missing_materials = {material: qty for material, qty in blueprint.materials_needed.items() 
                          if material not in materials_posesed or materials_posesed[material] < qty}
      if missing_materials:
        Konsola.print("Nie posiadasz składnikówi: ", "lred", line_end='')
        Konsola.print(str(missing_materials), 'lyellow')
        Konsola.print("Potrzebne składniki: " + str(blueprint.materials_needed))
        return 0 
      #TODO nie działa całe te
      for material, qty in blueprint.materials_needed.items():
        for item in self.equipment:
          if "material" in item.attr and item.attr["material"] == material:
            if item.stackable:
              item.amount -= qty
            else:
              self.equipment.remove_item(item)
            print("pobrano " + str(qty) + " " + item.name)
            continue 
      
      number_of_items = blueprint.number_of_items 

      for _ in range(number_of_items):
        item = Item.from_dict(blueprint.resulting_item)
        #TODO klasa ekwipunku //DONE :)
        self.equipment.add_item(item)
        if item.stackable():
          number_of_items = item.amount
      
      Helper.sleep(1)
      for description in blueprint.action_descriptions:
        Helper.sleep(0.5)
        Konsola.wrap(description)
      Helper.sleep(1)
      Konsola.print("Stworzyłeś " + str(number_of_items) + " sztuk ", "lgreen")
      Konsola.print(blueprint.resulting_item["name"], "lyellow")

  def to_dict(self):
    player = super().to_dict()
    return player
  
  @classmethod
  def from_dict(cls, data):
    mob_id = data["mob_id"]
    if mob_id in Mob.ids:
      raise ValueError(f"Duplicate mob ID found: {mob_id}")
    cls.ids[mob_id] = data["name"]
    eq = Equipment.from_dict(data["equipment"])
    slots = data["slots"]
    for key in slots:
      if slots[key] == {}:
        slots[key] = None
      else:
        slots[key] = Item.from_dict(slots[key])
    blueprints = [Blueprint.from_dict(blueprint) for blueprint in data["blueprints"]]

    return cls(data["mob_id"], data["x"], data["y"], data["z"], data["base_name"], data["name"], data["alias"], data["description"], data["lvl"], data["exp"], data["weight"], data["money"], data["race"], data["proficiency"], data["params"], data["stats"], data["skills"], eq, slots, data["knowledge"], data["journal"], True, True, blueprints, data["affiliation"])