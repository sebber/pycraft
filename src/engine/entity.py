from typing import Type

class Entity:
  _id_counter = 0
  
  def __init__(self):
    self.id = Entity._id_counter
    Entity._id_counter += 1
    self.components = {}
    
  def add_component[C](self, component: C) -> None:
    self.components[component.__class__] = component
  
  def get_component[C](self, component_class: Type[C]) -> C:
    return self.components.get(component_class)
  
  def remove_component[C](self, component_class) -> None:
    if component_class in self.components:
      del self.components[component_class]