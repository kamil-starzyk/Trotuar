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
    print("[1] Nowa gra")
    print("[5] Wyjdź z gry")
    print(" > ", end="")
  
  @classmethod
  def prompt(cls, player):
    command = []
    while not command:
      print("<HP: {}/{} Mana: {}/{}>".format(player.hp, player.hp_max, player.mana, player.mana_max), end="")
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
  def print(cls, text, f=f_reset, b=b_reset, line_end="\n"):
    color = cls.color_parser(f, b)

    if isinstance(text,int):
      text = str(text)

    print(color + text + c_reset, end=line_end)

  @classmethod
  def clear(cls):
    os.system('cls')

  @classmethod
  def print_random(cls, komunikat):
    print(random.choice(komunikat))

  @classmethod
  def hr(cls):
    print("-"*20)
  
  @classmethod
  def print_item_list(cls, items):
    print("|lp. | nazwa                   | waga  | cena  |")
    print(" ---- ------------------------- ------- ------- ")
    index = 1
    for i in items:
      print('|' + f_lwhite + f'{str(index): <4}' + c_reset+'|', end='')
      print(f_lwhite + f' {i.name: <24}' + c_reset+'|', end='')
      print(f_lwhite + f' {i.weight: <6}' + c_reset+'|', end='')
      print(f_lwhite + f' {i.price: <6}' + c_reset+'|')

  @classmethod
  def help(cls, command=''):
    print("Komenda: " + command)
    commands = {
      ("n", "north",  "8") : ["Przemieść się na północ", "Przemieść się jedną kratkę na północ jeśli, jest dostępne wyjście w tym kierunku oraz drzwi(jesli są) są otwarte"],
      ("e", "east",  "6") : ["Przemieść się na wschód", "Przemieść się jedną kratkę na wschód jeśli, jest dostępne wyjście w tym kierunku oraz drzwi(jesli są) są otwarte"],
      ("s", "south",  "2") : ["Przemieść się na południe", "Przemieść się jedną kratkę na południe, jeśli jest dostępne wyjście w tym kierunku oraz drzwi(jesli są) są otwarte"],
      ("w", "west",  "4") : ["Przemieść się na zachód", "Przemieść się jedną kratkę na zachód, jeśli jest dostępne wyjście w tym kierunku oraz drzwi(jesli są) są otwarte"],
      ("u", "north",  "5") : ["Wejdź pięto wyżej", "Przemieść się o jedno piętro w górę,jeśli jest dostępne wyjście w tym kierunku oraz drzwi(jesli są) są otwarte"],
      ("d", "north",  "0") : ["Zejdź piętro niżej", "Przemieść się o jedno piętro w dół, jeśli jest dostępne wyjście w tym kierunku oraz drzwi(jesli są) są otwarte"],
      ("whoami") : ["Wyświetl podstawowe informacje o sobie", "Wyświetl informacje o swoim imieniu rasie oraz opis"],
      ("whereami") : ["Pokaż swoje koordynaty", "Pokaż swoje współrzędne x, y, z oraz nazwę lokacji, w której się obecnie znajdujesz"],
      ("help", "pomoc", "?") : ["Pokaż swoje koordynaty", "Pokaż swoje współrzędne x, y, z oraz nazwę lokacji, w której się obecnie znajdujesz"],
      ("exit", "quit", "q") : ["Opuść grę", "Wyjdź z gry, ale wcześniej upewnij się, że zapisałeś swoje postępy, jeśli nie chcesz ich stracić"],
      ("help", "pomoc", "?") : ["Wyświetl pomoc", "Wyświetl wszystkie dostępne komendy, albo poznaj szczegóły konkretnej komendy wpisując po 'help' jej nazwę. Na przykład 'help rozmawiaj'"]
    }
    if not command:
      for c in commands:
        print(f'{str(c): <26}', end='')
        print(commands[c][0])
    else:
      for c in commands:
        if command in c:
          print(str(c), end=' - ')
          print(commands[c][1])

  
  @classmethod
  def color_parser(cls, f, b):
    if f != "reset":
      if f == "blue":
        color = f_blue
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