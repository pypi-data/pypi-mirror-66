from dataclasses import dataclass
from enum import Enum, auto
from typing import List

from recipebook.ingredient import Ingredient


@dataclass
class Time:
    @dataclass
    class Unit(Enum):
        SECONDS = "seconds"
        MINUTES = "minutes"
        HOURS = "hours"

    def __init__(self, quantity: float, unit: Unit):
        self.quantity: float = quantity
        self.unit: Time.Unit = unit

    def __str__(self):
        return f"{self.quantity} {self.unit.value}"


@dataclass
class Recipe:
    ingredients: List[Ingredient]
    instructions: List[str]

    def __init__(self, name: str, time: Time):
        self.name: str = name
        self.time: Time = time
