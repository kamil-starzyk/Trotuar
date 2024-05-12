from game import Game
from konsola import Konsola
from helper import Helper

game = Game()


while True:
  
  game.title_screen()
  player = game.player

  player.my_square.show_square()

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
  "przejdź":    player.use_passage,
  "przejdz":    player.use_passage,
  
  "podnies" :   player.pick_up,
  "podnieś" :   player.pick_up,
  "upuść" :     player.drop,
  "upusc" :     player.drop,
  "zjedz" :     player.use,
  "wypij" :     player.use,
  "zużyj" :     player.use,
  "użyj" :      player.use,
  "zuzyj" :     player.use,
  "uzyj" :      player.use,
  "zobacz" :    player.see,
  "załóż" :     player.equip,
  "zaloz" :     player.equip,
  "zdejmij" :   player.unequip,
  "ekwipunek" : player.show_equipment,
  "eq" :        player.show_equipment,
  "outfit" :    player.outfit,
  "ubiór" :     player.outfit,
  "ubior" :     player.outfit,
  "przeszukaj": player.search_utility,
  "search":     player.search_utility,

  "stats":      player.show_stats,
  "statystyki": player.show_stats,
  "params":     player.show_params,
  "parametry":  player.show_params,
  "odpoczywaj": player.rest,
  "odpocznij":  player.rest,
  "rest":       player.rest,
  "śpij":       player.sleep,
  "spij":       player.sleep,
  "sleep":      player.sleep,

  "oceń":       player.compare,
  "ocen":       player.compare,
  "compare":    player.compare,
  "rozmawiaj":  player.talk_to,
  "porozmawiaj":player.talk_to,
  "zabij":      player.kill,
  "podaruj":    player.give,
  "handel":     player.trade,
  "handluj":    player.trade,
  "trade":      player.trade,
  "zadania":    game.active_quests,
  "quests":     game.active_quests,
  
  "/" :         game.show_current_square,       
  "czas" :      game.time.show_time,
  "time" :      game.time.show_time,
  "whoami" :    player.whoami,
  "whereami" :  player.whereami,
  "help" :      Konsola.help,
  "?" :         Konsola.help,
  "save":       game.save,
  "zapisz":     game.save,
  "exit" :      game.end_game,
  "quit" :      game.end_game,
  "q" :         game.end_game,
  "colorama" :  Konsola.test_colorama,

  "exp":        player.add_exp
}

  while game.is_playing:
    prompt = Konsola.prompt(game.player)
    command = prompt[0]
    argument = prompt[1]

    seconds = 0

    if command in command_mapping:
      action = command_mapping[command]
      if isinstance(action, tuple):
        seconds = action[0](action[1])
      elif argument:
        # try:
           seconds = action(argument)
        # except TypeError:
        #   Konsola.print("To polecenie jest jednowyrazowe", "red")
      else: 
        # try:
          seconds = action()
        # except TypeError:
        #   Konsola.print("To polecenie wymaga więcej informacji!", "red")
    try:  
      int(seconds)
    except TypeError:
      seconds = 0
      
    game.update_state(seconds)