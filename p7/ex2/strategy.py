from abc import ABC, abstractmethod
from ex0.creature import Creature
from ex1.transform_capability import TransformCapability
from ex1.heal_capability import HealCapability


class InvalidCreature(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def act(self, creature: Creature) -> str:
        ...

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        ...


class NormalStrategy(BattleStrategy):
    strategy: str = "Normal"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, Creature)

    def act(self, creature: Creature) -> str:
        if self.is_valid(creature):
            return creature.attack()


class AggressiveStrategy(BattleStrategy):
    strategy: str = "Aggressive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> str:
        if not self.is_valid(creature):
            raise InvalidCreature(f"Battle error, aborting tournament: \
Invalid Creature '{creature.name}' for this aggressive strategy")

        if isinstance(creature, TransformCapability):
            return f"{creature.attack()}\n{creature.transform()}\
\n{creature.attack()}\n{creature.revert()}"


class DefensiveStrategy(BattleStrategy):
    strategy: str = "Defensive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> str:
        if not self.is_valid(creature):
            raise InvalidCreature(f"Battle error, aborting tournament: "
                                  f"Invalid Creature'{creature.name}' for this"
                                  f" aggressive strategy")

        if isinstance(creature, HealCapability):
            return f"{creature.attack()}\n{creature.heal()}"
