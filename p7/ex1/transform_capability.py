from abc import ABC, abstractmethod
from ex0.creature import Creature
from ex0.factory import CreatureFactory


class TransformCapability(ABC):
    def __init__(self, transformed: bool) -> None:
        self.transformed = transformed

    @abstractmethod
    def transform(self) -> str:
        ...

    @abstractmethod
    def revert(self) -> str:
        ...


class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Shifting", "Normal")
        TransformCapability.__init__(self, False)
        self.type_of_strategy = "Transform"

    def attack(self) -> str:
        if not self.transformed:
            return "Shiftling attacks normally."
        return "Shiftling performs a boosted strike!"

    def transform(self) -> str:
        self.transformed = True
        return "Shiftling shifts into a sharper form!"

    def revert(self) -> str:
        self.transformed = False
        return "Shiftling returns to normal."


class Morphagon(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Morphagon", "Normal/Dragon")
        TransformCapability.__init__(self, False)

    def attack(self) -> str:
        if not self.transformed:
            return "Morphagon attacks normally."
        return "Morphagon unleashes a devastating morph strike!"

    def transform(self) -> str:
        self.transformed = True
        return "Morphagon morphs into a dragonic battle form!"

    def revert(self) -> str:
        self.transformed = False
        return "Morphagon stabilizes its form."


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Shiftling:
        return Shiftling()

    def create_evolved(self) -> Morphagon:
        return Morphagon()
