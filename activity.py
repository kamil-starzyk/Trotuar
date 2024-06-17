from helper import Helper
from konsola import Konsola

class Activity:
  LIST_OF_ACTIVITIES = [
    "rest",
    "random_walk",
    "following_path",
    "fight",
    "stays_at_place"
  ]
  def __init__(self, type, description, importance, mob_id=0, destination=None):
    self.type = type
    self.description = description
    self.importance = importance #int 1-10
    self.mob_id = mob_id
    self.destination = destination

  def to_dict(self):
    return {
      "type": self.type,
      "description": self.description,
      "importance": self.importance,
      "mob_id": self.mob_id,
      "destination": self.destination
    }
  
  @classmethod
  def from_dict(cls, data):
    type = data.get("type")
    if type not in cls.LIST_OF_ACTIVITIES:
      raise ValueError(f"Invalid activity type: {type}")
    description = data.get("description")
    if not isinstance(description, list) or not description:
      raise ValueError("Description must be a non-empty list.")
    importance = data.get("importance", 1)
    mob_id = data.get("mob_id", 0)
    destination = data.get("destination", None)
    
    return cls(type, description, importance, mob_id, destination)