from konsola import Konsola
from helper import Helper

class AI:
  def __init__(self, schedule):
    self.schedule = schedule

  
  def to_dict(self):
    return {
      "schedule": self.schedule
    }

  @classmethod
  def from_dict(cls, data):
    return cls(data["schedule"])
  