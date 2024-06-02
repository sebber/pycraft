from typing import List
import pygame

from components import PositionComponent, RenderComponent, TargetPositionComponent
from engine.entity_manager import EntityManager
from engine.game import Game
from entity_factory import EntityFactory
from systems import MovementSystem

class MyGame(Game):
  def init(self):
    self.entity_manager = EntityManager()
    self.factory = EntityFactory(self.entity_manager)
    self.selected_entity: int = None
    
    self.factory.create_worker(50, 50)
    self.factory.create_worker(200, 250)
    self.factory.create_worker(120, 180)
    self.factory.create_worker(140, 80)
    self.factory.create_worker(400, 280)
    
    self.movement_system = MovementSystem(self.entity_manager)  
    
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
            
  def update(self, delta_time: float):
    self.movement_system.update(delta_time)
  
  def draw(self):
    self.screen.fill((0, 0, 0))
    
    for entity in self.entity_manager.get_entities_with_components(RenderComponent, PositionComponent):
      pos = self.entity_manager.get_component(entity, PositionComponent)
      render = self.entity_manager.get_component(entity, RenderComponent)
      pygame.draw.rect(
        self.screen,
        render.color,
        (pos.x, pos.y, render.width, render.height),
        2
      )
      if entity == self.selected_entity:
        pygame.draw.rect(
          self.screen,
          (255, 255, 255),
          (pos.x-2, pos.y-2, render.width+4, render.height+4),
          2
        )
      

if __name__ == "__main__":
  my_game = MyGame(800, 600, 60)
  my_game.run()