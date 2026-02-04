from myjson import MyJson

data = MyJson.load_json("data/init/demo.json")

loc1 = data["world"]["locations"][0]
number_of_squares = 0
number_of_items = 0
number_of_utilities = 0
utilities_id = []
for s in loc1["squares"]:
  number_of_squares+=1
  for i in s["items"]:
    number_of_items+=1
  
  for u in s["utilities"]:
    number_of_utilities+=1
    if u["id"] not in utilities_id:
      utilities_id.append(u["id"])
    else:
      print("Utility id duplicate: ", end="")
      print(u["id"], end=" ")
      print(u["name"])


print("Kratek: ", end="")
print(number_of_squares)

print("Utilsów: ", end="")
print(number_of_utilities)

def first_free_utility_id(utilities_ids):
  
  if not utilities_id:
    return 1

  ids = set(utilities_id)
  max_id = max(ids)

  for i in range(1, max_id + 1):
    if i not in ids:
      return i
  
  return max_id + 1
  
print("pierwsze wolne util id: ", end="")
print(first_free_utility_id(utilities_id))