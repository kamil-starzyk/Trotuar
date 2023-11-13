from konsola import Konsola

class Item:
  def __init__(self, type, alias, name, description, weight, price, attr):
    self.type = type
    self.alias = alias
    self.name = name
    self.description = description
    self.weight = weight
    self.price = price
    self.attr = attr

  def see_more(self):
    Konsola.print(self.name, "lcyan")
    Konsola.print(self.description, "lwhite")
    Konsola.print("Wartość: ", line_end='')
    Konsola.print(self.price, "lwhite")
    Konsola.print("Ciężar: ", line_end='')
    Konsola.print(self.weight, "lwhite")
    if self.amount > 1:
      Konsola.print("Ilość: ", line_end='')
      Konsola.print(self.amount, "lwhite")
    Konsola.print("Atrybuty:", "lwhite")
    for k, v in self.attr.items():
      Konsola.print(" " + k, line_end=': ')
      Konsola.print(v, "lwhite")
  
  @property
  def name_and_count(self):
    if "amount" in self.attr and self.attr["amount"] > 1:
      return self.name + " ( " + str(self.attr["amount"]) + " )"
    else:
      return self.name

  @property
  def amount(self):
    if "amount" in self.attr:
      return self.attr["amount"]
    return 1
  
  @amount.setter
  def amount(self, value):
    if "amount" in self.attr:
      self.attr["amount"] = value
  
  def stackable(self):
    if "amount" in self.attr:
      return True
    return False

  def to_dict(self):
    return {
      "type": self.type,
      "alias" : self.alias,
      "name": self.name,
      "description": self.description,
      "weight": self.weight,
      "price": self.price,
      "attr": self.attr
    }
  
  @classmethod
  def from_dict(cls, data):
    return cls(data["type"], data["alias"], data["name"], data["description"], data["weight"], data["price"], data["attr"])
  
  @classmethod
  def unstack(cls, item, amount_to_unstack):
    attr = item.attr.copy()
    attr["amount"] = amount_to_unstack
    item.amount -= amount_to_unstack
    return cls(item.type, item.alias, item.name, item.description, item.weight, item.price, attr)