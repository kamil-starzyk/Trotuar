import os

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