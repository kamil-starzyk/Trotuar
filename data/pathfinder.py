import os
import random
import time

class Mob:
  def __init__(self, symbol, x, y, mapa):
    self.symbol = symbol
    self.x = x
    self.y = y
    self.map = mapa

    self.is_searching_for_route = False
    self.dest_x = None
    self.dest_y = None

  def is_on_square(self, x, y):
    if self.x == x and self.y == y:
      return True
    return False
  
  def random_walk(self):
    exits = self.my_square.exits
    e = random.choice(exits)
    self.move_in_direction(e)

  def move_in_direction(self, direction):
    if direction in self.my_square.exits:
      match direction:
        case "n":
          self.y -= 1
        case "e":
          self.x += 1
        case "s":
          self.y += 1
        case "w":
          self.x -= 1
      return direction
    return 0
  
  def add_destination(self, x, y):
    if self.map.get_square_at(x, y):
      self.dest_x = x
      self.dest_y = y
      self.is_searching_for_route = True
      return True
    print("There is no square with this coordinates")
    return 0

  def recursive_pathfinder(self, current_x, current_y, visited):
    x = current_x
    y = current_y

    if (x, y) in visited:
      return 0
    if (x, y) == (self.dest_x, self.dest_y):
      return []

    visited.append((x, y))
    square = self.map.get_square_at(x, y)
    if square:
      exits = square.exits
      for direction in exits:
        if direction == "n":
          path = self.recursive_pathfinder(x, y-1, visited)
          if isinstance(path, list):
            path.append(direction)
            return path
        if direction == "e":
          path = self.recursive_pathfinder(x+1, y, visited)
          if isinstance(path, list):
            path.append(direction)
            return path
        if direction == "s":
          path = self.recursive_pathfinder(x, y+1, visited)
          if isinstance(path, list):
            path.append(direction)
            return path
        if direction == "w":
          path = self.recursive_pathfinder(x-1, y, visited)
          if isinstance(path, list):
            path.append(direction)
            return path
      return 0

    else:
      return 0


  @property
  def my_square(self):
    return self.map.get_square_at(self.x, self.y)



class Square:
  def __init__(self, x, y, exits):
    self.x = x
    self.y = y
    self.exits = exits
  
  def draw_square(self, symbol=''):
    fill = ""
    if "s" not in self.exits:
      fill = "__"
    else:
      fill = "  "
    if symbol:
      fill = symbol[0] + fill[1:]
    print(fill, end='')
    if "e" not in self.exits:
      print("|", end='')
    else:
      print(" ", end='')
  
class Map:
  def __init__(self, size_x, size_y):
    self.size_x = size_x
    self.size_y = size_y
    self.squares = []

  def add_square(self, square):
    if not self.get_square_at(square.x, square.y):
      self.squares.append(square)
    else:
      raise ValueError(f"Duplikat ({square.x}, {square.y})")
  
  def get_square_at(self, x, y):
    for sq in self.squares:
      #print(f'SQ: ({sq.x}, {sq.y}) == For: {x}, {y})')
      if sq.x == x and sq.y == y:
        return sq
    return None
  
  def draw_map(self, mob):
    os.system('cls')
    print("  x: ", end='')
    for x in range(self.size_x):
      print(f'{x: <3}', end='')
    print('')
    print("y: ", end='')
    print(" __"*self.size_x)
    for y in range(self.size_y):
      print(f"{y: <3}|", end='')
      for x in range(self.size_x):
        sq = self.get_square_at(x,y)
        if sq and mob.is_on_square(x, y):
          sq.draw_square(mob.symbol)
        elif sq and mob.is_searching_for_route and mob.dest_x == x and mob.dest_y == y:
          sq.draw_square("X")
        elif sq:
          sq.draw_square()
        else:
          pass
          print("##|", end='')
      print('')

def int_input(message, min_val=None, max_val=None):
  while True:
    try:
      user_input = int(input(message))
      if (min_val is None or user_input >= min_val) and (max_val is None or user_input <= max_val):
        return user_input
      else:
        print("Wprowadź liczbę z zakresu (" + str(min_val) + " - " + str(max_val))
    except ValueError:
      print("Wprowadź liczbę")

squares = []
squares.append(Square(1, 0, ['s', 'e']))
squares.append(Square(2, 0, ['w', 'e']))
squares.append(Square(3, 0, ['w', 's']))

squares.append(Square(0, 1, ['e']))
squares.append(Square(1, 1, ['e', 'n', 'w']))
squares.append(Square(2, 1, ['w', 's']))
squares.append(Square(3, 1, ['n', 'e']))
squares.append(Square(4, 1, ['w', 's']))

squares.append(Square(0, 2, ['e']))
squares.append(Square(1, 2, ['e', 's', 'w']))
squares.append(Square(2, 2, ['n', 'w']))
squares.append(Square(4, 2, ['n', 'e']))
squares.append(Square(5, 2, ['w', 's']))

squares.append(Square(1, 3, ['n', 's']))
squares.append(Square(4, 3, ['e', 's']))
squares.append(Square(5, 3, ['w', 'n']))

squares.append(Square(1, 4, ['s', 'n']))
squares.append(Square(4, 4, ['s', 'n']))

squares.append(Square(0, 5, ['s']))
squares.append(Square(1, 5, ['n', 's']))
squares.append(Square(2, 5, ['e', 's']))
squares.append(Square(3, 5, ['w', 's']))
squares.append(Square(4, 5, ['n', 's']))

squares.append(Square(0, 6, ['n', 's']))
squares.append(Square(1, 6, ['n', 's']))
squares.append(Square(2, 6, ['n', 's']))
squares.append(Square(3, 6, ['n', 's', 'e']))
squares.append(Square(4, 6, ['n', 'w']))

squares.append(Square(0, 7, ['n', 'e']))
squares.append(Square(1, 7, ['n', 'e', 'w']))
squares.append(Square(2, 7, ['n', 'w']))
squares.append(Square(3, 7, ['n', 'e']))
squares.append(Square(4, 7, ['e', 'w']))
squares.append(Square(5, 7, ['w']))


mapa = Map(6, 8)


for sq in squares:
  # print(f'({sq.x}, {sq.y})')
  mapa.add_square(sq)


mob = Mob("P", 0, 0, mapa)

# for _ in range(10):
#   mob.random_walk()
#   mapa.draw_map(mob)
#   time.sleep(0.3)

mapa.draw_map(mob)

mobx = int_input("Podaj X postaci: ", 0, mapa.size_x-1)
moby = int_input("Podaj Y postaci: ", 0, mapa.size_y-1)

mob.x = mobx
mob.y = moby

mapa.draw_map(mob)

x = int_input("Podaj X celu: ", 0, mapa.size_x-1)
y = int_input("Podaj Y celu: ", 0, mapa.size_y-1)

mob.add_destination(x,y)
visited = []
paths = []
path = 1
while path:
  mob.x = mobx
  mob.y = moby
  if (mob.x, mob.y) in visited:
    visited.remove((mob.x, mob.y)) 
  path = mob.recursive_pathfinder(mob.x, mob.y, visited)
  if path in paths:
    path = 0
  if isinstance(path, list):
    path.reverse()
    paths.append(path)


if len(paths) == 0:
  print("Nie ma ścieżki do tego celu")
  exit()
for path in paths:
  mob.x = mobx
  mob.y = moby
  print(path)
  time.sleep(1)
  for step in path:
    mob.move_in_direction(step)
    mapa.draw_map(mob)
    time.sleep(0.3)

shortest_path = min(paths, key=len)
print("Najkrótsza ścieżka to: ", end='')
print(shortest_path)





