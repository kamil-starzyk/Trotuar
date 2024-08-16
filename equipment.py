from helper import Helper
from konsola import Konsola
from item import Item

class Equipment:
  def __init__(self, items):
    self.items = items
  
  def show(self):
    Konsola.print_item_list(self.items)
  
  def is_item_in_eq(self, item):
    Helper.is_item_in_list(item, self.items)

  def add_item(self, item):
    item_in_eq = self.is_item_in_eq(item)
    if item.stackable() and item_in_eq:
      item_in_eq.amount += item.amount
    else:
      self.items.append(item)
    return item

  def remove_item(self, item, amount=1):
    if item.stackable():
      if amount == item.amount:
        self.items.remove(item)
      else:
        item = Item.unstack(item, amount)
    else:
      self.items.remove(item)
    
    return item
     
    

  def to_dict(self):
    return [item.to_dict() for item in self.items]
  
  @classmethod
  def from_dict(cls, data):
    items = [Item.from_dict(item_data) for item_data in data]
    return cls(items)