from components import BoundingBoxComponent, PositionComponent, RenderComponent, TargetPositionComponent, VelocityComponent
from engine.entity_manager import EntityManager

class EntityFactory:
  def __init__(self, entity_manager: EntityManager):
    self.entity_manager = entity_manager
    
  def create_worker(self, pos_x: int, pos_y: int):
    width = 50
    height = 50
    
    entity = self.entity_manager.create_entity()
    self.entity_manager.add_component(entity, PositionComponent(pos_x, pos_y))
    self.entity_manager.add_component(entity, VelocityComponent(100))
    self.entity_manager.add_component(entity, RenderComponent((0, 220, 0), width, height))
    self.entity_manager.add_component(entity, TargetPositionComponent(pos_x, pos_y))
    self.entity_manager.add_component(entity, BoundingBoxComponent(width, height))