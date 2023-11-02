from konsola import Konsola

class Item:
  def __init__(self, type, alias, name, description, weight, price, attributes):
    self.type = type
    self.alias = alias
    self.name = name
    self.description = description
    self.weight = weight
    self.price = price
    self.attributes = attributes

  def see_more(self):
    Konsola.print(self.name, "lmagenta")
    Konsola.print(self.description, "lwhite")
    Konsola.print("Wartość: ", line_end='')
    Konsola.print(self.price, "lwhite")
    Konsola.print("Ciężar: ", line_end='')
    Konsola.print(self.weight, "lwhite")

  def to_dict(self):
    return {
      "type": self.type,
      "alias" : self.alias,
      "name": self.name,
      "description": self.description,
      "weight": self.weight,
      "price": self.price,
      "attributes": self.attributes
    }
  
  @classmethod
  def from_dict(cls, data):
    return cls(data["type"], data["alias"], data["name"], data["description"], data["weight"], data["price"], data["attributes"])
  