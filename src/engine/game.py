import sys
import pygame

class Game:
  def __init__(self, width: int, height: int, target_fps: int):
    pygame.init()
    self.screen = pygame.display.set_mode((width, height))
    self.clock = pygame.time.Clock()
    self.running = False
    self.target_fps = target_fps
        
  def exit(self) -> None:
    self.running = False
          
  def init() -> None:
    pass
    
  def update(self, _dt: float) -> None:
    pass
  
  def draw() -> None:
    pass
  
  def run(self) -> None:
    self.running = True
    self.init()
    
    while self.running:
      self.handle_events()
      delta_time = self.clock.tick(self.target_fps) / 1000.0
      self.update(delta_time)
      self.draw()
      pygame.display.flip()
      
    pygame.quit()
    sys.exit()