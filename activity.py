from helper import Helper
from konsola import Konsola

class Activity:
  LIST_OF_ACTIVITIES = [
    "rest",
    "random_walk",
    "following_path",
    "fight",
    "stays_at_place",
    "prepares_workshop"
  ]
  def __init__(self, type, description, importance, area=None, mob_id=0, destination=None):
    self.type = type
    self.description = description
    self.importance = importance #int 1-10
    self.area = area
    self.mob_id = mob_id
    self.destination = destination

  def to_dict(self):
    return {
      "type": self.type,
      "description": self.description,
      "importance": self.importance,
      "area": self.area,
      "mob_id": self.mob_id,
      "destination": self.destination
    }
  
  @classmethod
  def from_dict(cls, data):
    print(data["type"])
    type = data.get("type")
    if type not in cls.LIST_OF_ACTIVITIES:
      raise ValueError(f"Invalid activity type: {type}")
    description = data.get("description")
    if not isinstance(description, list) or not description:
      raise ValueError("Description must be a non-empty list.")
    importance = data.get("importance", 1)
    area = data.get("area", None)
    mob_id = data.get("mob_id", 0)
    destination = data.get("destination", None)
    
    return cls(type, description, importance, area, mob_id, destination)