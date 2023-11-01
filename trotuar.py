from game import Game
from konsola import Konsola

game = Game()
game.title_screen()

player = game.player
player.current_location.find_square(2,2,0).items[0].pick_up(player)

print("Brawo! Udało Ci się rozpocząć grę")

item = None
mob = None

command_mapping = {
  "n" :         (player.move_in_direction, "n"),
  "north" :     (player.move_in_direction, "n"),
  "8" :         (player.move_in_direction, "n"),
  "e" :         (player.move_in_direction, "e"),
  "east" :      (player.move_in_direction, "e"),
  "6" :         (player.move_in_direction, "e"),
  "s" :         (player.move_in_direction, "s"),
  "south" :     (player.move_in_direction, "s"),
  "2" :         (player.move_in_direction, "s"),
  "w" :         (player.move_in_direction, "w"),
  "west" :      (player.move_in_direction, "w"),
  "4" :         (player.move_in_direction, "w"),
  
  "podnies":    (player.pick_up, item),

  "whoami" :    player.whoami,
  "whereami" :  player.whereami,
  "help" :      Konsola.help,
  "?" :         Konsola.help,
  "exit" :      game.end_game,
  "quit" :      game.end_game,
  "q" :         game.end_game

}

while game.is_playing:
  prompt = Konsola.prompt(game.player)
  command = prompt[0]
  argument = prompt[1]

  #todo finding item

  if command in command_mapping:
    action = command_mapping[command]
    if isinstance(action, tuple):
      action[0](action[1])
    elif argument:
      action(argument)
    else: action()
  
