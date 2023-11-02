from game import Game
from konsola import Konsola

game = Game()
game.title_screen()

player = game.playerc

print("Brawo! Udało Ci się rozpocząć grę")

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
  
  "podnies" :   player.pick_up,
  "podnieś" :   player.pick_up,
  "upuść" :     player.drop,
  "upusc" :     player.drop,
  "equipment" : player.show_equipment,

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

  if command in command_mapping:
    action = command_mapping[command]
    if isinstance(action, tuple):
      action[0](action[1])
    elif argument:
      action(argument)
    else: action()
  
