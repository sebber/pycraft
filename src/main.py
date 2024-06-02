from typing import List
import pygame

from engine.entity import Entity
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
  def update(self, entities: List[Entity], delta_time: float):
    for entity in entities:
      pos = entity.get_component(PositionComponent)
      velocity = entity.get_component(VelocityComponent)
      target_pos = entity.get_component(TargetPositionComponent)
      
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
    # self.player_pos = pygame.Vector2(
    #   self.screen.get_width() / 2,
    #   self.screen.get_height() / 2
    # )
    # self.player_speed = 500
    
    self.entities: List[Entity] = []
    self.selected_entity = None
    self.create_entity(50, 50, 50, 50, 100, (255, 0, 0))
    self.create_entity(200, 200, 50, 50, 200, (0, 255, 0))
    
    self.movement_system = MovementSystem()
    
  def create_entity(self, x, y, width, height, velocity, color):
    entity = Entity()
    entity.add_component(PositionComponent(x, y))
    entity.add_component(RenderComponent(color, width, height))
    entity.add_component(VelocityComponent(velocity))
    entity.add_component(TargetPositionComponent(x, y))
    self.entities.append(entity)    
    
  def select_entity(self, mouse_pos):
    for entity in self.entities:
      pos = entity.get_component(PositionComponent)
      render = entity.get_component(RenderComponent)
      if (pygame.Rect(pos.x, pos.y, render.width, render.height).collidepoint(mouse_pos)):
        self.selected_entity = entity
        print(f"Entity {entity.id} selected")
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
      target = self.selected_entity.get_component(TargetPositionComponent)
      target.x, target.y = target_pos
      target.has_target = True
            
  def update(self, dt: float):
    self.movement_system.update(self.entities, dt)
    pass
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #   self.player_pos.y -= self.player_speed * dt
    # if keys[pygame.K_s]:
    #   self.player_pos.y += self.player_speed * dt
    # if keys[pygame.K_a]:
    #   self.player_pos.x -= self.player_speed * dt
    # if keys[pygame.K_d]:
    #   self.player_pos.x += self.player_speed * dt
  
  def draw(self):
    self.screen.fill((0, 0, 0))
    # pygame.draw.circle(self.screen, "red", self.player_pos, 40)
    
    for entity in self.entities:
      pos = entity.get_component(PositionComponent)
      render = entity.get_component(RenderComponent)
      pygame.draw.rect(self.screen, render.color, (pos.x, pos.y, render.width, render.height), 2)
      if entity == self.selected_entity:
        pygame.draw.rect(self.screen, (255, 255, 255), (pos.x, pos.y, render.width, render.height), 2)
      

if __name__ == "__main__":
  my_game = MyGame(800, 600, 60)
  my_game.run()