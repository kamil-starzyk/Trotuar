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
    pass

  def remove_item(self, item):
    pass
    

  def to_dict(self):
    return [item.to_dict() for item in self.items]
  
  @classmethod
  def from_dict(cls, data):
    items = [Item.from_dict(item_data) for item_data in data]
    return cls(items)