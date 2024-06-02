from abc import ABC, abstractmethod

from engine.entity_manager import EntityManager

class UpdateSystem(ABC):
  def __init__(self, entity_manager: EntityManager):
    self.entity_manager = entity_manager
    
  @abstractmethod
  def update(self, delta_time: float):
    pass
  
class DrawSystem(ABC):
  def __init__(self, entity_manager: EntityManager):
    self.entity_manager = entity_manager
    
  @abstractmethod
  def draw(self, screen):
    pass