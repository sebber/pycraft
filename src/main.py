from typing import List
import pygame

from components import PositionComponent, RenderComponent, SelectedComponent, TargetPositionComponent
from engine.entity_manager import EntityManager
from engine.game import Game
from engine.world import World
from entity_factory import EntityFactory
from systems import CollisionDetectionSystem, CollisionResolutionSystem, MovementSystem, RenderSystem

class MyGame(Game):
  def init(self):
    self.world = World()
    self.world.add_system(MovementSystem)
    self.world.add_system(RenderSystem)
    self.world.add_system(CollisionDetectionSystem)
    self.world.add_system(CollisionResolutionSystem)
    self.factory = EntityFactory(self.world.entity_manager)
    
    self.factory.create_worker(50, 50)
    self.factory.create_worker(200, 250)
    self.factory.create_worker(120, 180)
    self.factory.create_worker(140, 80)
    self.factory.create_worker(400, 280)
    
  def select_entity(self, mouse_pos, multi_select = False):
    e_manager = self.world.entity_manager
    for entity in e_manager.get_entities_with_components(PositionComponent, RenderComponent):
      pos = e_manager.get_component(entity, PositionComponent)
      render = e_manager.get_component(entity, RenderComponent)
      if (pygame.Rect(pos.x, pos.y, render.width, render.height).collidepoint(mouse_pos)):
        if not multi_select:
          selected_entities = list(e_manager.get_entities_with_component(SelectedComponent))
          for selected in selected_entities:
            e_manager.remove_component(selected, SelectedComponent)
        
        e_manager.add_component(entity, SelectedComponent())
        print(f"Entity {entity} selected")
  
  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left mouse button
          keys = pygame.key.get_pressed()
          shift = keys[pygame.K_LSHIFT]
          self.select_entity(event.pos, shift)
        elif event.button == 3:  # Right mouse button
          self.move_selected_entity(event.pos)
      
  def move_selected_entity(self, target_pos):
    for entity in self.world.entity_manager.get_entities_with_component(SelectedComponent):
      print(f"Entity {entity} has SelectedComponent")
      target = self.world.entity_manager.get_component(
        entity,
        TargetPositionComponent
      )
      target.x, target.y = target_pos
      target.has_target = True
            
  def update(self, delta_time: float):
    self.world.update(delta_time)
  
  def draw(self, screen: pygame.Surface):
    self.screen.fill((0, 0, 0))
    self.world.draw(screen)
      

if __name__ == "__main__":
  my_game = MyGame(800, 600, 60)
  my_game.run()