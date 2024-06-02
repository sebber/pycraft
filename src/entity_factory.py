from components import PositionComponent, RenderComponent, TargetPositionComponent, VelocityComponent
from engine.entity_manager import EntityManager

class EntityFactory:
  def __init__(self, entity_manager: EntityManager):
    self.entity_manager = entity_manager
    
  def create_worker(self, pos_x: int, pos_y: int):
    entity = self.entity_manager.create_entity()
    self.entity_manager.add_component(entity, PositionComponent(pos_x, pos_y))
    self.entity_manager.add_component(entity, VelocityComponent(100))
    self.entity_manager.add_component(entity, RenderComponent((0, 220, 0), 50, 50))
    self.entity_manager.add_component(entity, TargetPositionComponent(pos_x, pos_y))