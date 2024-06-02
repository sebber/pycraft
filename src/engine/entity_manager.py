from typing import List, Type
class EntityManager:
  def __init__(self):
    self.next_entity_id = 1
    self.entities: dict[int] = {}
    self.components = {}
    
  def create_entity(self):
    entity_id = self.next_entity_id
    self.next_entity_id += 1
    self.entities[entity_id] = []
    return entity_id
  
  def add_component[C](self, entity_id: int, component: C):
    component_type = type(component)
    if entity_id not in self.entities:
      self.entities[entity_id] = []
    self.entities[entity_id].append(component)
    
    if component_type not in self.components:
      self.components[component_type] = {}
    self.components[component_type][entity_id] = component
    
  def get_component[C](self, entity_id: int, component_type: Type[C]) -> C:
    return self.components.get(component_type, {}).get(entity_id)      
    
  def remove_component[C](self, entity_id: int, component_type: Type[C]):
    if entity_id in self.entities:
      self.entities[entity_id] = [c for c in self.entities[entity_id] if not isinstance(c, component_type)]
    if component_type in self.components:
      if entity_id in self.components[component_type]:
        del self.components[component_type][entity_id]
    
  def get_entities_with_component[C](self, component_type: C) -> set[int]:
    return self.components.get(component_type, {}).keys()

  def get_entities_with_components[C](self, *component_types: C) -> set[int]:
    if not component_types:
      return []

    result_set = set(self.get_entities_with_component(component_types[0]))

    for component_type in component_types[1:]:
        result_set &= set(self.get_entities_with_component(component_type))

    return result_set