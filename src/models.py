from typing import Dict, Union
from constants import *

class Entity:
    """Base class shared between Territory and AgeGender."""
    def __init__(self):
        self.purposes: Dict[str, Dict[str, Union[int, float]]] = {
            f: {"poblacion": 0, "porcentaje": 0.0} for f in PurposeStruct.PURPOSES
        }

    def update_purpose(self, purpose: str, population: int = None, percentage: float = None):
        """Updates the population or percentage for a given purpose."""
        if purpose in self.purposes:
            if population is not None:
                self.purposes[purpose]["poblacion"] = population
            if percentage is not None:
                self.purposes[purpose]["porcentaje"] = percentage

class Territory(Entity):
    """Represents a territory and tracks the highest percentage recorded across its purposes."""
    highest_percentage: float = 0.0

    def __init__(self, name: str):
        super().__init__()
        self.name = name    # Store the name of the territory

    def update_purpose(self, purpose: str, population: int = None, percentage: float = None):
        """Overrides the method to also track the highest percentage."""
        super().update_purpose(purpose=purpose, population=population, percentage=percentage)
        if purpose != EXCLUDED_CATEGORY and percentage is not None:
            Territory.highest_percentage = max(Territory.highest_percentage, percentage)

class AgeGender(Entity):
    """Represents an age group with a specified gender."""
    def __init__(self, age: str, gender: str):
        super().__init__()
        self.age = age
        self.gender = gender
