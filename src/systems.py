from components import PositionComponent, TargetPositionComponent, VelocityComponent
from engine.entity_manager import EntityManager
from engine.systems import UpdateSystem


class MovementSystem(UpdateSystem):
  def update(self, delta_time: float):
    for entity in self.entity_manager.get_entities_with_components(PositionComponent, VelocityComponent, TargetPositionComponent):
      pos = self.entity_manager.get_component(entity, PositionComponent)
      velocity = self.entity_manager.get_component(entity, VelocityComponent)
      target_pos = self.entity_manager.get_component(entity, TargetPositionComponent)
      
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

