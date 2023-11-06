import time
import re
from datetime import datetime
from os import listdir


class Helper:
  

  @classmethod
  def sleep(cls, seconds):
    time.sleep(seconds)
  
  @classmethod
  def datetime(cls):
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%y%m%d%H%M")

    return formatted_date

  @classmethod
  def open_saves(cls):
    paths = listdir("./data/saves")
    paths.remove(".gitkeep")
    return list(reversed(paths))

  @classmethod
  def get_new_gameplay_number(cls):
    highest_number = 0
    for filename in cls.open_saves():
      match = re.search(r'_(\d+)(?=\.\w+$)', filename)
      if match:
        number = match.group(1)
        number = int(number)
        if number > highest_number:
          highest_number = number
    return highest_number+1

  @classmethod
  def find_item(cls, item_list, item_name):
    hit = []
    for i in item_list:
      if item_name in i.alias:
        hit.append(i)
    
    if len(hit) == 1:
      return hit[0]
    elif len(hit) > 1:
      print("O co Ci dokładnie chodzi?")
      return cls.chose_one_item(hit)
    else:
      return 0
  
  @classmethod
  def chose_one_item(cls, item_list):
    for i in range(len(item_list)):
      print(str(i+1)+". "+item_list[i].name)
    while True:
      item_number = int(input())-1
      for i in range(len(item_list)):
        if item_number == i:
          return item_list[item_number]
  