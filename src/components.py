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
    
class SelectedComponent:
  def __init__(self):
    self.selected = True
    
class BoundingBoxComponent:
  def __init__(self, width: int, height: int):
    self.width = width
    self.height = height
    
class CollisionComponent:
  def __init__(self, other_entity):
    print(f"poop")
    self.other_entity = other_entity