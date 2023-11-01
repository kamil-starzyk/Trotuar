class Item:
  def __init__(self, type, name, description, weight, price, attributes):
    self.type = type
    self.name = name
    self.description = description
    self.weight = weight
    self.price = price
    self.attributes = attributes

  def look_up(self):
    print(self.name)
    print(self.description)

  def to_dict(self):
    return {
      "type": self.type,
      "name": self.name,
      "description": self.description,
      "weight": self.weight,
      "price": self.price,
      "attributes": self.attributes
    }
  
  @classmethod
  def from_dict(cls, data):
    return cls(data["type"], data["name"], data["description"], data["weight"], data["price"], data["attributes"])
  