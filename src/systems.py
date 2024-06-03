from pygame import Surface
import pygame
from components import BoundingBoxComponent, CollisionComponent, PositionComponent, RenderComponent, SelectedComponent, TargetPositionComponent, VelocityComponent
from engine.entity_manager import EntityManager
from engine.systems import DrawSystem, UpdateSystem


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

  
class CollisionDetectionSystem(UpdateSystem):
  def update(self, delta_time: float):
    entities = list(self.entity_manager.get_entities_with_components(PositionComponent, BoundingBoxComponent))
    for i in range(len(entities)):
      for j in range(i + 1, len(entities)):
        entity_a = entities[i]
        entity_b = entities[j]
                
        pos_a = self.entity_manager.get_component(entity_a, PositionComponent)
        bbox_a = self.entity_manager.get_component(entity_a, BoundingBoxComponent)
        pos_b = self.entity_manager.get_component(entity_b, PositionComponent)
        bbox_b = self.entity_manager.get_component(entity_b, BoundingBoxComponent)

        if self.check_collision(pos_a, bbox_a, pos_b, bbox_b):
          self.entity_manager.add_component(entity_a, CollisionComponent(entity_b))
          self.entity_manager.add_component(entity_b, CollisionComponent(entity_a))
      
  def check_collision(self, pos_a, bbox_a, pos_b, bbox_b):
    return (pos_a.x < pos_b.x + bbox_b.width and
            pos_a.x + bbox_a.width > pos_b.x and
            pos_a.y < pos_b.y + bbox_b.height and
            pos_a.y + bbox_a.height > pos_b.y)
    
class CollisionResolutionSystem(UpdateSystem):
  def update(self, delta_time):
    for entity_id in list(self.entity_manager.get_entities_with_component(CollisionComponent)):
      collision = self.entity_manager.get_component(entity_id, CollisionComponent)
      if not collision:
        return
      other_entity = collision.other_entity

      pos = self.entity_manager.get_component(entity_id, PositionComponent)
      bbox = self.entity_manager.get_component(entity_id, BoundingBoxComponent)
      other_pos = self.entity_manager.get_component(other_entity, PositionComponent)
      other_bbox = self.entity_manager.get_component(other_entity, BoundingBoxComponent)

      if pos and bbox and other_pos and other_bbox:
        overlap_x, overlap_y = self.calculate_overlap(pos, bbox, other_pos, other_bbox)
        self.resolve_collision(pos, bbox, other_pos, other_bbox, overlap_x, overlap_y)

      self.entity_manager.remove_component(entity_id, CollisionComponent)
      self.entity_manager.remove_component(other_entity, CollisionComponent)

  def calculate_overlap(self, pos_a, bbox_a, pos_b, bbox_b):
    overlap_x = min(pos_a.x + bbox_a.width, pos_b.x + bbox_b.width) - max(pos_a.x, pos_b.x)
    overlap_y = min(pos_a.y + bbox_a.height, pos_b.y + bbox_b.height) - max(pos_a.y, pos_b.y)
    return overlap_x, overlap_y

  def resolve_collision(self, pos_a, bbox_a, pos_b, bbox_b, overlap_x, overlap_y):
    # Resolve collision along the axis of the smallest overlap
    if overlap_x < overlap_y:
      if pos_a.x < pos_b.x:
        pos_a.x -= overlap_x / 2
        pos_b.x += overlap_x / 2
      else:
        pos_a.x += overlap_x / 2
        pos_b.x -= overlap_x / 2
    else:
      if pos_a.y < pos_b.y:
        pos_a.y -= overlap_y / 2
        pos_b.y += overlap_y / 2
      else:
        pos_a.y += overlap_y / 2
        pos_b.y -= overlap_y / 2

class RenderSystem(DrawSystem):
  def draw(self, screen: Surface):
    for entity in self.entity_manager.get_entities_with_components(RenderComponent, PositionComponent):
      pos = self.entity_manager.get_component(entity, PositionComponent)
      render = self.entity_manager.get_component(entity, RenderComponent)
      pygame.draw.rect(
        screen,
        render.color,
        (pos.x, pos.y, render.width, render.height),
        2
      )
      selected = self.entity_manager.get_component(entity, SelectedComponent)
      if selected and selected.selected:
        pygame.draw.rect(
          screen,
          (255, 255, 255),
          (pos.x-2, pos.y-2, render.width+4, render.height+4),
          2
        )
