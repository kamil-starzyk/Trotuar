from konsola import Konsola
self = None
# KAMIENIE MILOWE
if "Przybicie do brzegu" in self.milestones:
  #Helper.sleep(0.5)
  Konsola.wrap("Rozpoczynasz swoją przygodę! Czynność, którą będziesz wykonywał najczęściej to poruszanie się pomiędzy sąsiednimi lokalizacjami. Każda lokalizacja ma swoją [i]nazwę[/i], [i]opis[/i] oraz dostępne [i]wyjścia[/i]. Aby się przemieścić wpisz jako prompt nazwę dostępnego kierunku np([i]east[/i]), albo jej jednoliterowy skrót (np. [i]e[/i]). Na początek jednak spróbuj porozmawiać z Jackiem. Aby to zrobić wpisz [i]rozmawiaj jacek[/i].")
  Konsola.hr()
  #Helper.sleep(1)
  self.milestones.remove("Przybicie do brzegu")
if "Worek węgla" in self.milestones:
  jacek = next((mob for mob in self.player.current_location.mobs if mob.name == "Spławiacz Jacek"), None)
  jacek.take("worek węgla", True)
  jacek.drop("worek węgla", True)
  Konsola.print("Jacek wyjmuje worek węgla z łodzi", "lmagenta")
  Konsola.hr()
  #Helper.sleep(1.5)
  self.show_current_square()
  Konsola.hr()
  #Helper.sleep(0.5)
  Konsola.wrap("Jeśli na twojej lokalizacji znajdują się jakieś przedmioty albo osoby, z którymi możesz wejść w interakcję, to zostaną one wypisane pod pozyją [i]Istoty[/i] lub [i]Przedmioty[/i]. Pewne interaktywne obiekty znajdujące się na lokalizacji są wskazane w jej opisie. Szukaj podświetlonych nazw (np. [i]łódź[/i]). Dla różnych obiektów są dostępne różne komendy, ale zawsze możesz wspisać polecenie [i]zobacz[/i] (np. [i]zobacz worek węgla[/i]) aby dowiedzieć się o obiekcie coś więcej i poznać dostępne komendy. ")
  Konsola.hr()
  #Helper.sleep(1)
  self.milestones.remove("Worek węgla")
  self.milestones.append("Worek węgla 2")

worek_podniesiony = False
worek_quest = next((q for q in self.quests if q.id == 4), None)
if worek_quest:
  for obj in quest.objectives:
    if obj["type"] == "item_in_eq" and obj["progress"] == 1:
      worek_podniesiony = True

if "Worek węgla 2" in self.milestones and worek_podniesiony:
  Konsola.hr()
  Konsola.wrap("Aktywne zadania możesz podejrzeć za pomocą komendy [i]zadania[/i]. Aby wyświetlić postęp konkretnego zadania dopisz jego id. (np. [i]zadania 4[/i]). ")
  Konsola.hr()
  #Helper.sleep(0.5)
  self.milestones.remove("Worek węgla 2")
  self.milestones.append("Worek węgla 3")

if "Worek węgla 3" in self.milestones and self.player.is_on_square(6,2,1):
  Konsola.hr()
  Konsola.wrap("Brawo! Odnalazłeś kuźnię! Teraz, aby przekazać przedmiot właściwej osobie musisz skorzystać z komendy [i]podaruj[/i] (np. [i]podaruj worek węgla[/i]). Nie musisz wpisywać komu. Jeśli na lokacji jest tylko jedna osoba nie będzie problemu. Za to kiedy potencjalnych odbiorców byłoby więcej - gra zapyta o kogo Ci chodzi. ")
  Konsola.hr()
  Konsola.wrap("Teraz wracaj nad rzekę po kolejne zadania!")
  Konsola.hr()
  #Helper.sleep(0.5)
  self.milestones.remove("Worek węgla 3")
  self.milestones.append("Worek węgla 4")

worek_oddany = False
if worek_quest:
  for obj in quest.objectives:
    if obj["type"] == "return_item" and obj["progress"] == 1:
      worek_oddany = True

if "Worek węgla 4" in self.milestones and worek_oddany:
  Konsola.hr()
  Konsola.wrap("Wspaniale! Udało Ci się ukończyć pierwsze zadanie! Zadania są jednym ze źódeł zdobywania doświadczenia. Aby zobaczyć obecny postęp swojej postaci użyj komendy [i]whoami[/i]. Wyświetla ona podstawowe dane na twój temat, w tym obecny poziom, zdobyte doświadczenie oraz inne #TODO. ")
  Konsola.hr()
  self.milestones.remove("Worek węgla 4")

  ##Helper.sleep(0.5)

if "Towary dla karczmarza" in self.milestones:
  jacek = next((mob for mob in self.player.current_location.mobs if mob.name == "Spławiacz Jacek"), None)
  jacek.take("beczka piwa", False)
  jacek.drop("beczka piwa", False)
  #Helper.sleep(2)
  Konsola.print("Jacek wyjmuje beczkę piwa z łodzi", "lmagenta")
  jacek.take("skrzynka wina", False)
  jacek.drop("skrzynka wina", False)
  #Helper.sleep(1)
  Konsola.print("Jacek wyjmuje skrzynkę wina z łodzi", "lmagenta")
  jacek.take("butelka gorzałki", False)
  jacek.drop("butelka gorzałki", False)
  #Helper.sleep(0.5)
  Konsola.print("Jacek wyjmuje butelki gorzałki z łodzi", "lmagenta")
  #Helper.sleep(1)
  self.show_current_square()
  self.milestones.remove("Towary dla karczmarza")
  self.milestones.append("Ciężkie rzeczy")
if "Ciężkie rzeczy" in self.milestones and self.player.overloaded:
  Konsola.hr()
  Konsola.wrap("Uważaj na wagę swojego ekwipunku. Jego zawartość możesz sprawdzić komendą [i]ekwipunek[/i] lub [i]eq[/i]. Zobaczysz tam listę swoich rzeczy, ich sumaryczną masę oraz swój udźwig w postaci: [i]Udźwig: 50 / 40(80)[/i]. W tym przypadku gracz niesie 50 funtów ekwipunku, czyli 10 więcej niż jego zwykły udźwig i 30 poniżej maksymalnego udźwigu. Im większe przeciążenie ponad normalny udźwig, tym szybciej się męczysz. Swoją aktualną staminę możesz zobaczyć na prompcie jako St: lub używając komendy [i]parametry[/i]/[i]params[/i].  ")
  self.milestones.remove("Ciężkie rzeczy")
