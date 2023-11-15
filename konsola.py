from colorama import init, Fore, Back, Style
import math
import os
import msvcrt
import keyboard
import textwrap 
import random

#czasami wyświetlało kod koloru zamiast koloru bez tej linijki
init(convert=True) 

f_reset = Fore.RESET
b_reset = Back.RESET
c_reset = Fore.RESET + Back.RESET

f_blue = Fore.BLUE
f_black = Fore.BLACK
f_cyan = Fore.CYAN
f_green = Fore.GREEN
f_magenta = Fore.MAGENTA
f_red = Fore.RED
f_white = Fore.WHITE
f_yellow = Fore.YELLOW
f_lblack = Fore.LIGHTBLACK_EX
f_lblue = Fore.LIGHTBLUE_EX
f_lcyan = Fore.LIGHTCYAN_EX
f_lgreen = Fore.LIGHTGREEN_EX
f_lmagenta = Fore.LIGHTMAGENTA_EX
f_lred = Fore.LIGHTRED_EX
f_lwhite = Fore.LIGHTWHITE_EX
f_lyellow = Fore.LIGHTYELLOW_EX

b_blue = Back.BLUE
b_cyan = Back.CYAN
b_green = Back.GREEN
b_magenta = Back.MAGENTA
b_red = Back.RED
b_white = Back.WHITE
b_yellow = Back.YELLOW
b_lblack = Back.LIGHTBLACK_EX
b_lblue = Back.LIGHTBLUE_EX
b_lcyan = Back.LIGHTCYAN_EX
b_lgreen = Back.LIGHTGREEN_EX
b_lmagenta = Back.LIGHTMAGENTA_EX
b_lred = Back.LIGHTRED_EX
b_lwhite = Back.LIGHTWHITE_EX
b_lyellow = Back.LIGHTYELLOW_EX

class Konsola:
  def __init__(self):
    pass

  @classmethod
  def show_title_screen(cls, version):
    os.system('cls')
    print("Trotuar v. " + version)
    print("Witaj")
    print("---------------")
    cls.print("[1] Nowa gra", "red")
    print("[2] Wczytaj")
    print("[3] Demo")
    print("[5] Wyjdź z gry")
  
  @classmethod
  def prompt(cls, player):
    command = []
    while not command:
      print(f_lmagenta, end="")
      print("<HP: {}/{} Mana: {}/{}> ".format(player.hp, player.hp_max, player.mana, player.mana_max), end="")
      print(c_reset, end="")

      decision = input().lower()
      command = decision.split()
    if len(command) == 1:
      argument = ''
    else:
      argument = ' '.join(command[1:])	
    result = []
    result.append(command[0])
    result.append(argument)
    return result
  
  @classmethod
  def int_input(cls, min_val=None, max_val=None):
    while True:
      try:
        user_input = int(input(" > "))
        if (min_val is None or user_input >= min_val) and (max_val is None or user_input <= max_val):
          return user_input
        else:
          print("Wprowadź liczbę z zakresu (" + str(min_val) + " - " + str(max_val))
      except ValueError:
        print("Wprowadź liczbę")

  @classmethod
  def print(cls, text, f=f_reset, b=b_reset, line_end="\n"):
    color = cls.color_parser(f, b)

    text = str(text)

    print(color + text + c_reset, end=line_end)

  @classmethod
  def wrap(cls, text_to_wrap, f=f_reset, b=b_reset):
    """
    This is ridiculous. I tried regex, finding index etc. But everything f**ks up. 
    Manulat iteration shouldn't be to-go option but WHATEVER at this point. Nonetheless
    wrap() wraps text to 100 characters wide lines, avoiding breaking words. 
    If it encounters [i]text[/i] it highlights it.
    """
    wrapper = textwrap.TextWrapper(width=100)
    lines_list = wrapper.wrap(text=text_to_wrap)
    text_to_highlight = "\n".join(lines_list)
    
    highlighted_parts = {}
    start_tag = "[i]"
    end_tag = "[/i]"
    start_index = 0
    end_index = 0
    
    start_index = text_to_highlight.find(start_tag, end_index)
    if start_index > 0:
      normal_text = text_to_highlight[0:start_index]
      highlighted_parts[normal_text] = False

    while start_index != -1 and end_index != -1:
      if start_index != -1:
        end_index = text_to_highlight.find(end_tag, start_index + len(start_tag))
        if end_index != -1:
          # Extract the content between [i] and [/i]
          highlighted_text = text_to_highlight[start_index + len(start_tag):end_index]

          highlighted_parts[highlighted_text] = True

          start_index = text_to_highlight.find(start_tag, end_index)  

          normal_text = text_to_highlight[end_index + len(end_tag): start_index]
          highlighted_parts[normal_text] = False


    for k, v in highlighted_parts.items():
      if v:
        cls.print(k, "lwhite", b, line_end='')
      else:
        cls.print(k, "white", b, line_end='')
    print('')




  @classmethod
  def clear(cls):
    os.system('cls')

  @classmethod
  def print_random(cls, komunikat):
    print(random.choice(komunikat))

  @classmethod
  def hr(cls):
    print("-"*24)

  @classmethod
  def damage_given(cls, by_player, mob, damage):
    if by_player:
      print("Zadałeś " + f_lwhite + mob.name + c_reset + f_lred + " " + str(damage) + c_reset + " obrażeń")
    else:
      print(f_lwhite + mob.name + c_reset + " zadał Ci " + f_lred + str(damage) + c_reset + " obrażeń")
  
  @classmethod
  def print_item_list(cls, items):
    print("|lp. | nazwa                   | waga  | wartość  |")
    print(" ---- ------------------------- ------- ---------- ")
    index = 1
    weight = 0
    amount = 0
    price = 0
    for i in items:
      print('|' + f_lwhite + f'{str(index): <4}' + c_reset+'|', end='')
      print(f_lwhite + f' {i.name_and_count: <24}' + c_reset+'|', end='')
      print(f_lwhite + f' {round(i.weight * i.amount, 2): <6}' + c_reset+'|', end='')
      print(f_lwhite + f' {i.price * i.amount: <9}' + c_reset+'|')
      index+=1
      amount += i.amount
      weight += i.weight * i.amount
      price += i.price * i.amount
    if index > 2:
      print(" ---- ------------------------- ------- ---------- ")
      print(" Przedmiotów: " + f'{str(amount): <17}' + f'| {str(round(weight,2)): <6}' + f'| {str(price): <9}' + '|')
    print(" ---- ------------------------- ------- ---------- ")
  @classmethod
  def print_stats(cls, mob):
    print("STATYSTYKI " + f_lwhite + mob.name + c_reset)
    cls.hr()

    def print_stat(attribute_name, attribute_value):
      items_effect = attribute_value - mob.stats[attribute_name]
      items_effect_str = str(items_effect) if items_effect < 0 else "+" + str(items_effect)
      print(f"{attribute_name.capitalize(): <15} {mob.stats[attribute_name]} ({items_effect_str})")

    print_stat("strength", mob.strength)
    print_stat("attack", mob.attack)
    print_stat("defence", mob.defence)
    print_stat("speed", mob.speed)
    print_stat("dexterity", mob.dexterity)
    print_stat("endurance", mob.endurance)

  @classmethod
  def print_params(cls, mob):
    print("PARAMETRY " + f_lwhite + mob.name + c_reset)
    cls.hr()

    cls.print_param("hp", mob.hp, mob.hp_max, "lred")
    cls.print_param("stamina", mob.stamina, mob.stamina_max, "lyellow")
    cls.print_param("mana", mob.mana, mob.mana_max, "lblue")
    cls.print_param("satiation", mob.satiation, mob.satiation_max, "lgreen")
    cls.print_param("hydration", mob.hydration, mob.hydration_max, "lcyan")

    print(c_reset)

  @classmethod
  def print_param(cls, attribute_name, attribute_value, attribute_max, bg_color):
    color = cls.color_parser("black", bg_color)
    text = " " + attribute_name.upper() + ": " + str(attribute_value) + " / " + str(attribute_max)
    numbers_of_pixels = int((attribute_value / attribute_max)*24)
    for i in range(24):
      if i < numbers_of_pixels:
        print(color, end='')
        try:
          print(text[i], end='')
        except IndexError:
          print(" ", end='')
      else:
        print(b_lblack + f_black, end='')
        try:
          print(text[i], end='')
        except IndexError:
          print(" ", end='')
    print(c_reset)

  @classmethod
  def help(cls, command=''):
    print("Komenda: " + command)
    commands = {
      ("n", "north",  "8") : ["Przemieść się na północ", "Przemieść się jedną kratkę na północ jeśli, jest dostępne wyjście w tym kierunku oraz drzwi(jesli są) są otwarte"],
      ("e", "east",  "6") : ["Przemieść się na wschód", "Przemieść się jedną kratkę na wschód jeśli, jest dostępne wyjście w tym kierunku oraz drzwi(jesli są) są otwarte"],
      ("s", "south",  "2") : ["Przemieść się na południe", "Przemieść się jedną kratkę na południe, jeśli jest dostępne wyjście w tym kierunku oraz drzwi(jesli są) są otwarte"],
      ("w", "west",  "4") : ["Przemieść się na zachód", "Przemieść się jedną kratkę na zachód, jeśli jest dostępne wyjście w tym kierunku oraz drzwi(jesli są) są otwarte"],
      ("u", "up",  "5") : ["Wejdź pięto wyżej", "Przemieść się o jedno piętro w górę,jeśli jest dostępne wyjście w tym kierunku oraz drzwi(jesli są) są otwarte"],
      ("d", "down",  "0") : ["Zejdź piętro niżej", "Przemieść się o jedno piętro w dół, jeśli jest dostępne wyjście w tym kierunku oraz drzwi(jesli są) są otwarte"],
      ("/") : ["Pokaż miejsce gdzie jesteś", "Jesli po dłuższej rozmowie, albo walce nie wiesz gdzie jesteś możesz wyświetlić ponownie opis swojej kratki"],
      ("whoami") : ["Wyświetl podstawowe informacje o sobie", "Wyświetl informacje o swoim imieniu rasie oraz opis"],
      ("whereami") : ["Pokaż swoje koordynaty", "Pokaż swoje współrzędne x, y, z oraz nazwę lokacji, w której się obecnie znajdujesz"],
      ("ekwipunek", "eq") : ["Pokaż zawartość ekwipunku", "Pokaż listę przedmiotów jakie masz przy sobie oraz ich wagę i cenę"],
      ("outfit", "ubiór", "ubior") : ["Pokaż co masz na sobie", "Pokaż listę slotów twojej postaci oraz jakie przedmioty są przypisane do każdego z nich"],
      ("podnieś", "podnies") : ["Podnieś przedmiot", "Podnieś dany przedmiot, jeśli znajduje się w tym samym miejscu co ty. \nSKŁADNIA: <podnieś nazwa przedmiotu>"],
      ("upuść", "upusc") : ["Upuść przedmiot", "Upuść dany przedmiot, jeśli znajduje się w twoim ekwipunku. \nSKŁADNIA: <upuść nazwa przedmiotu>"],
      ("załóż", "zaloz"): ["Załóż przedmiot", "Załóż przedmiot jeśli znajduje się w twoim ekwipunku.\nSKŁADNIA: <załóż nazwa przedmiotu>"],
      ("help", "pomoc", "?") : ["Pokaż swoje koordynaty", "Pokaż swoje współrzędne x, y, z oraz nazwę lokacji, w której się obecnie znajdujesz"],
      ("exit", "quit", "q") : ["Opuść grę", "Wyjdź z gry, ale wcześniej upewnij się, że zapisałeś swoje postępy, jeśli nie chcesz ich stracić"],
      ("help", "pomoc", "?") : ["Wyświetl pomoc", "Wyświetl wszystkie dostępne komendy, albo poznaj szczegóły konkretnej komendy wpisując po 'help' jej nazwę. Na przykład 'help rozmawiaj'"]
    }
    if not command:
      for c in commands:
        print(f'{str(c): <30}', end='')
        print(commands[c][0])
    else:
      for c in commands:
        if command in c:
          print(str(c), end=' - ')
          print(commands[c][1])

  @classmethod
  def you_died(cls):
    print("             _+_")
    print("           _/ * \_")
    print("  /\     _/  \_/  \_     /\\")
    print("  ||_&__/..-- 0 --..\__&_||")
    print("  --_______--- ---_______--")
    cls.print("   POLEGŁEŚ NA POLU CHWAŁY", "lyellow")
    print("   (') (') (') (') (') (') ")
    print("    W   W   W   W   W   W ")

  @classmethod
  def direction_translator(cls, direction):
    direction_map = {
      ("n", "north"): "na północ",
      ("e", "east"): "na wschód",
      ("s", "south"): "na południe",
      ("w", "west"): "na zachód",
      ("u", "up"): "w górę",
      ("d", "down"): "w górę",
    }
    for d in direction_map:
      if direction in d:
        return direction_map[d]
  @classmethod
  def color_parser(cls, f, b):
    if f != "reset":
      if f == "blue":
        color = f_blue
      elif f == "black":
        color = f_black
      elif f == "cyan":
        color = f_cyan
      elif f == "green":
        color = f_green
      elif f == "magenta":
        color = f_magenta
      elif f == "red":
        color = f_red
      elif f == "white":
        color = f_white
      elif f == "yellow":
        color = f_yellow
      elif f == "lblack":
        color = f_lblack	
      elif f == "lblue":
        color = f_lblue
      elif f == "lcyan":
        color = f_lcyan
      elif f == "lgreen":
        color = f_lgreen
      elif f == "lmagenta":
        color = f_lmagenta
      elif f == "lred":
        color = f_lred
      elif f == "lwhite":
        color = f_lwhite
      elif f == "lyellow":
        color = f_lyellow
      else: 
        color = Fore.RESET
    else: 
      color = Fore.RESET
    if b != "reset":
      if b == "blue":
        color += b_blue
      elif b == "cyan":
        color += b_cyan
      elif b == "green":
        color += b_green
      elif b == "magenta":
        color += b_magenta
      elif b == "red":
        color += b_red
      elif b == "white":
        color += b_white
      elif b == "yellow":
        color += b_yellow
      elif b == "lblack":
        color += b_lblack	
      elif b == "lblue":
        color += b_lblue
      elif b == "lcyan":
        color += b_lcyan
      elif b == "lgreen":
        color += b_lgreen
      elif b == "lmagenta":
        color += b_lmagenta
      elif b == "lred":
        color += b_lred
      elif b == "lwhite":
        color += b_lwhite
      elif b == "lyellow":
        color += b_lyellow
      else: 
        color += Back.RESET
    else: 
      color += Back.RESET
    return color

  @classmethod
  def test_colorama(cls):
    colors = dict(Fore.__dict__.items())
    backs = dict(Back.__dict__.items())

    for color in colors.keys():
      print(colors[color] + f"{color}")
    
    for back in backs.keys():
      print(backs[back] + f"{back}",end='')
      print(c_reset)
