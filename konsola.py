import os
import math

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
			argument = '-'.join(command[1:])	
		result = []
		result.append(command[0])
		result.append(argument)
		return result

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