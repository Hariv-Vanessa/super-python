from ex1.heal_capability import HealingCreatureFactory
from ex1.transform_capability import TransformCreatureFactory


if __name__ == "__main__":
    print("Testing Creature with healing capability\nbase:")
    healing_creature = HealingCreatureFactory()
    sproutling = healing_creature.create_base()
    print(sproutling.describe())
    print(sproutling.attack())
    print(sproutling.heal())
    print("evolved:")
    bloomelle = healing_creature.create_evolved()
    print(bloomelle.describe())
    print(bloomelle.attack())
    print(bloomelle.heal())

    print("\nTesting Creature with transform capability\nbase:")
    transform_creature = TransformCreatureFactory()
    shiftling = transform_creature.create_base()
    print(shiftling.describe())
    print(shiftling.attack())
    print(shiftling.transform())
    print(shiftling.attack())
    print(shiftling.revert())
    print("evolved:")
    morphagon = transform_creature.create_evolved()
    print(morphagon.describe())
    print(morphagon.attack())
    print(morphagon.transform())
    print(morphagon.attack())
    print(morphagon.revert())
