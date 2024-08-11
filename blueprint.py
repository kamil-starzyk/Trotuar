from helper import Helper
from konsola import Konsola
from item import Item

class Blueprint:
  def __init__(self, type, name, content, time, skills_needed, materials_needed, tools_needed, resulting_item, number_of_items):
    self.type = type
    self.name = name
    self.content = content
    self.time = time
    self.skills_needed = skills_needed
    self.materials_needed = materials_needed
    self.tools_needed = tools_needed
    self.resulting_item = resulting_item
    self.number_of_items = number_of_items
  
  def read(self):
    Konsola.print(self.name, "lyellow")
    Konsola.wrap(self.content)
    Konsola.hr()
    Konsola.print("Potrzebne umiejętności:", "lwhite")
    for k, v in self.skills_needed.items():
      print(" " + k + " - " + str(v))
    Konsola.print("Potrzebne składniki:", "lwhite")
    for k, v in self.materials_needed.items():
      print(" " + k + " - " + str(v) + "szt.")
    Konsola.print("Potrzebne narzędzia:", "lwhite")
    for t in self.tools_needed:
      print(" " + t)
    

  def to_dict(self):
    return {
      "type": self.type,
      "name": self.name,
      "content": self.content,
      "time": self.time,
      "skills_needed": self.skills_needed,
      "materials_needed": self.materials_needed,
      "tools_needed": self.tools_needed,
      "resulting_item": self.resulting_item.to_dict(),
      "number_of_items": self.number_of_items
    }
  
  @classmethod
  def from_dict(cls, data):
    return cls(data["type"], data["name"], data["content"], data["time"], data["skills_needed"], data["materials_needed"], data["tools_needed"], data["resulting_item"], data["number_of_items"])