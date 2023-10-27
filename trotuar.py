from game import Game

game = Game()

game.title_screen()
print(game.world.locations[0].squares[0].exits["n"])

print("Brawo! Udało Ci się rozpocząć grę")