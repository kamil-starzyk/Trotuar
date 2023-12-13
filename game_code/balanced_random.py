import random

class BalancedRandom:
  direction = 1

  @classmethod
  def random(cls, min_value, max_value, equalizer):
    """
    equalizer must be float from range 0 to 1
    """
    if equalizer < 0 or equalizer > 1:
      return -1
    values_range = max_value - min_value
    adjust_by = int(values_range * (0.5*equalizer))
    if cls.direction == 1:
      cls.direction *= -1
      return random.randint(min_value, max_value-adjust_by)
    else:
      cls.direction *= -1
      return random.randint(min_value+adjust_by, max_value)

class BiasedRandom:
  bias_from_zero = 0
  bias_from_one = 0

  @classmethod
  def random(cls, min_value, max_value, threshold, multiplier):
    """
    threshold is value past which outcome changes i.e. accuracy 
    multiplier must be float from range 0 to 1
    """
    if threshold < min_value or threshold > max_value:
      return -1

    if multiplier < 0 or multiplier > 1:
      return -1
    
    
    random_value = random.randint(min_value+cls.bias_from_zero, max_value-cls.bias_from_one)
    if random_value < threshold:
      cls.bias_from_zero += int(random_value*multiplier)
      cls.bias_from_one = 0
    else:
      cls.bias_from_one += int(random_value*multiplier)
      cls.bias_from_zero = 0
    
    return random_value

accuracy = -1
while not 0 <= accuracy <=100:
  accuracy_input = input("Podaj celność (0-100): ")
  try:
    accuracy = int(accuracy_input)
  except ValueError:
    print("Podaj liczbę!")
    continue
  if not 0 <= accuracy <=100:
    print("Podaj liczbę z zakresu!")

print("Podana celność: " + str(accuracy))

random_methods = [
  "basic_random",
  "balanced_random 0",
  "balanced_random 0.333",
  "balanced_random 0.666",
  "balanced_random 1",
  "biased_random 0",
  "biased_random 0.333",
  "biased_random 0.666",
  "biased_random 1",
]

for method in random_methods:
  print("------------------------------")
  print("Metoda: " + method)
  print("")

  hits = 0
  misses = 0

  length_of_series_of_hits = 0
  length_of_series_of_misses = 0

  longest_series_of_hits = 0
  longest_series_of_misses = 0

  series_of_hits = []
  series_of_misses = []

  for _ in range(2):
    chance = -1
    if method == "basic_random":
      chance = random.randint(0, 100)
    elif method == "balanced_random 0":
      chance = BalancedRandom.random(0, 100, 0)
    elif method == "balanced_random 0.333":
      chance = BalancedRandom.random(0, 100, 0.333)
    elif method == "balanced_random 0.666":
      chance = BalancedRandom.random(0, 100, 0.666)
    elif method == "balanced_random 1":
      chance = BalancedRandom.random(0, 100, 1)
    elif method == "biased_random 0":
      chance = BiasedRandom.random(0, 100, accuracy, 0)
    elif method == "biased_random 0.333":
      chance = BiasedRandom.random(0, 100, accuracy, 0.333)
    elif method == "biased_random 0.666":
      chance = BiasedRandom.random(0, 100, accuracy, 0.666)
    elif method == "biased_random 1":
      chance = BiasedRandom.random(0, 100, accuracy, 1)
    
    if chance < 0:
      print("Nastąpił błąd!")
      break

    if chance < accuracy:
      hits += 1
      length_of_series_of_misses = 0
      length_of_series_of_hits += 1
      series_of_hits.append(length_of_series_of_hits)
      if length_of_series_of_hits > longest_series_of_hits:
        longest_series_of_hits = length_of_series_of_hits
    else:
      misses += 1
      length_of_series_of_misses += 1
      length_of_series_of_hits = 0
      series_of_misses.append(length_of_series_of_misses)
      if length_of_series_of_misses > longest_series_of_misses:
        longest_series_of_misses = length_of_series_of_misses
  try:
    average_length_of_series_of_hits = sum(series_of_hits) / len(series_of_hits)
  except ZeroDivisionError:
    average_length_of_series_of_hits = 0
  try:
    average_length_of_series_of_misses = sum(series_of_misses) / len(series_of_misses)
  except ZeroDivisionError:
    average_length_of_series_of_misses = 0

  print("Trafień:" + str(hits))
  print("Pudeł:" + str(misses))
  print("Średnia długość serii trafień: " + str(round(average_length_of_series_of_hits, 2)))
  print("Średnia długość serii pudeł: " + str(round(average_length_of_series_of_misses, 2)))
  print("Najdłuższa seria trafień: " + str(longest_series_of_hits))
  print("Najdłuższa seria pudeł: " + str(longest_series_of_misses))

