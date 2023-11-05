from game import Game
from konsola import Konsola

game = Game()
game.title_screen()

player = game.player

player.my_square().show_square()

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
  "u" :         (player.move_in_direction, "u"),
  "up" :        (player.move_in_direction, "u"),
  "5" :         (player.move_in_direction, "u"),
  "d" :         (player.move_in_direction, "d"),
  "down" :      (player.move_in_direction, "d"),
  "0" :         (player.move_in_direction, "d"),
  
  "podnies" :   player.pick_up,
  "podnieś" :   player.pick_up,
  "upuść" :     player.drop,
  "upusc" :     player.drop,
  "zobacz" :    player.see_item,
  "załóż" :     player.equip,
  "zaloz" :     player.equip,
  "ekwipunek" : player.show_equipment,
  "eq" :        player.show_equipment,
  "outfit" :    player.outfit,
  "ubiór" :     player.outfit,
  "ubior" :     player.outfit,

  "rozmawiaj":  player.talk_to,

  "whoami" :    player.whoami,
  "whereami" :  player.whereami,
  "help" :      Konsola.help,
  "?" :         Konsola.help,
  "save":       game.save,
  "zapisz":     game.save,
  "exit" :      game.end_game,
  "quit" :      game.end_game,
  "q" :         game.end_game,
  "colorama" :  Konsola.test_colorama
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
  
