import time

class Helper:
  

  @classmethod
  def sleep(cls, seconds):
    time.sleep(seconds)

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
  