from npc import Npc
from player import Player
from place import Place
from item import Item

def place_exists(name, places):
  for p in places:
    if p.name.lower() == name:
      return p, "SUCCESS"
    return False, "FAIL__NO_PLACE"

player = Player("Ozjasz", 3, 3, 50, 100, 80, 100, 30, 100, 33)
places = []
infirmary = Place("Lecznica", "Skromne miejsce, w którym leczy się chorych. Stoi tu kilka łóżek.", 5, 0, "treat", 10)
places.append(infirmary)


is_playing = True

print("Co chcesz zrobić?")
while is_playing:
  command = input(" > ").lower().split()
  print(command)
  if len(command) == 0:
    print("Napisz coś")
    continue

  if command[0] == "q":
    is_playing = False
  elif command[0] == "go":
    place, message = place_exists(command[1], places)
    if not place:
      print(message)
      continue
    if not player.go_to_coordinates(place.x, place.y):
      print(message)
      continue
    print("Udałeś się do " + place.name)
    