from components import PositionComponent, TargetPositionComponent, VelocityComponent
from engine.entity_manager import EntityManager


class MovementSystem:
  def update(self, entity_manager: EntityManager, delta_time: float):
    for entity in entity_manager.entities:
      pos = entity_manager.get_component(entity, PositionComponent)
      velocity = entity_manager.get_component(entity, VelocityComponent)
      target_pos = entity_manager.get_component(entity, TargetPositionComponent)
      
      if pos and target_pos.has_target:
        dx = target_pos.x - pos.x
        dy = target_pos.y - pos.y
        distance = (dx**2 + dy**2)**0.5
        if distance < 1:
          target_pos.has_target = False
        else:
          dir_x = dx / distance
          dir_y = dy / distance
          pos.x += dir_x * velocity.velocity * delta_time
          pos.y += dir_y * velocity.velocity * delta_time
