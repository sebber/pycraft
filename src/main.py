from typing import List
import pygame

from engine.entity_manager import EntityManager
from engine.game import Game

class PositionComponent:
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y

class RenderComponent:
  def __init__(self, color: tuple[int, int, int], width: int, height: int):
    self.color = color
    self.width = width
    self.height = height

class TargetPositionComponent:
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y
    self.has_target = False

class VelocityComponent:
  def __init__(self, velocity: int):
    self.velocity = velocity

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

class MyGame(Game):
  def init(self):
    self.entity_manager = EntityManager()
    self.selected_entity: int = None
    
    entity1 = self.entity_manager.create_entity()
    self.entity_manager.add_component(entity1, PositionComponent(200, 50))
    self.entity_manager.add_component(entity1, VelocityComponent(100))
    self.entity_manager.add_component(entity1, TargetPositionComponent(200, 50))
    self.entity_manager.add_component(entity1,
                                      RenderComponent((255, 0, 0), 50, 50))
    
    entity2 = self.entity_manager.create_entity()
    self.entity_manager.add_component(entity2, PositionComponent(270, 250))
    self.entity_manager.add_component(entity2, VelocityComponent(200))
    self.entity_manager.add_component(entity2, 
                                      TargetPositionComponent(270, 250))
    self.entity_manager.add_component(entity2,
                                      RenderComponent((0, 255, 0), 50, 50))
    
    self.movement_system = MovementSystem()  
    
  def select_entity(self, mouse_pos):
    for entity in self.entity_manager.entities:
      pos = self.entity_manager.get_component(entity, PositionComponent)
      render = self.entity_manager.get_component(entity, RenderComponent)
      if (pygame.Rect(pos.x, pos.y, render.width, render.height).collidepoint(mouse_pos)):
        self.selected_entity = entity
        print(f"Entity {entity} selected")
        return
      self.selected_entity = None
  
  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left mouse button
          self.select_entity(event.pos)
        elif event.button == 3:  # Right mouse button
          self.move_selected_entity(event.pos)
      
  def move_selected_entity(self, target_pos):
    if self.selected_entity:
      target = self.entity_manager.get_component(
        self.selected_entity,
        TargetPositionComponent
      )
      target.x, target.y = target_pos
      target.has_target = True
            
  def update(self, dt: float):
    self.movement_system.update(self.entity_manager, dt)
    pass
  
  def draw(self):
    self.screen.fill((0, 0, 0))
    
    for entity in self.entity_manager.entities:
      pos = self.entity_manager.get_component(entity, PositionComponent)
      render = self.entity_manager.get_component(entity, RenderComponent)
      pygame.draw.rect(self.screen, render.color, (pos.x, pos.y, render.width, render.height), 2)
      if entity == self.selected_entity:
        pygame.draw.rect(self.screen, (255, 255, 255), (pos.x-1, pos.y-1, render.width+2, render.height+2), 2)
      

if __name__ == "__main__":
  my_game = MyGame(800, 600, 60)
  my_game.run()