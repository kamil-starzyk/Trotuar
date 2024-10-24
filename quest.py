class Quest:
  def __init__(self, id, name, description, objectives, reward, status, knowledge_entry):
    self.id = id
    self.name = name
    self.description = description
    self.objectives = objectives 
    self.reward = reward
    self.status = status # 0 - not yet taken / 1 - active / 2 -finished
    self.knowledge_entry = knowledge_entry
  
  def is_finished(self):
    if self.status == 1:
      return all(obj["progress"] >= obj["amount"] for obj in self.objectives)
    return 0
  
  def print_reward(self):
    print("Nagroda:", end=' ')
    if "money" in self.reward:
      print(str(self.reward["money"]) + " złota", end=' ')
    if "exp" in self.reward:
      print(str(self.reward["exp"]) + " doświadczenia", end=' ')
    print('')
    
  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "description": self.description,
      "objectives": self.objectives,
      "reward": self.reward,
      "status": self.status,
      "knowledge_entry": self.knowledge_entry
    }
  
  @classmethod
  def from_dict(cls, data):
    return cls(data["id"], data["name"], data["description"], data["objectives"], data["reward"], data["status"], data["knowledge_entry"])