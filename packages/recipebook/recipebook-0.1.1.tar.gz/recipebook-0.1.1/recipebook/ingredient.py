from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class Ingredient:
    class UnitOfMeasurement(Enum):
        NA = "n/a"
        Ounces = "oz"
        Pounds = "lbs"
        Grams = "g"
        Kilograms = "kg"
        Millilitres = "ml"
        Cups = "cup"

    name: str
    quantity: float
    unit: UnitOfMeasurement

    def __init__(self, name: str, quantity: float, unit: UnitOfMeasurement):
        self.name = name
        self.quantity = quantity
        self.unit = unit
