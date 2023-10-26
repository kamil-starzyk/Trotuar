from location import Location

class World:
  def __init__(self, locations):
    self.locations = locations

  def to_dict(self):
    return {
      "locations": [location.to_dict() for location in self.locations]
    }
  
  @classmethod
  def from_dict(cls, data):
    locations = [Location.from_dict(location_data) for location_data in data["locations"]]

    return cls(locations) 