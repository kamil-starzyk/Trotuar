class Quest:
  def __init__(self, id, name, description, objectives, reward, status):
    self.id = id
    self.name = name
    self.description = description
    self.objectives = objectives 
    self.reward = reward
    self.status = status
    
  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "description": self.description,
      "objectives": self.objectives,
      "reward": self.reward,
      "status": self.status
    }
  
  @classmethod
  def from_dict(cls, data):
    return cls(data["id"], data["name"], data["description"], data["objectives"], data["reward"], data["status"])