from typing import List
from engine.entity_manager import EntityManager
from engine.systems import DrawSystem, UpdateSystem


class World:
  def __init__(self):
    self.entity_manager = EntityManager()
    self.systems: List[UpdateSystem | DrawSystem] = []
    
  def add_system(self, system: UpdateSystem | DrawSystem):
    self.systems.append(system(self.entity_manager))
    
  def update(self, delta_time: float):
    for system in self.systems:
      if (isinstance(system, UpdateSystem)):
        system.update(delta_time)
  
  def draw(self, screen):
    for system in self.systems:
      if (isinstance(system, DrawSystem)):
        system.draw(screen)