from ex0 import CreatureFactory, FlameFactory, AquaFactory
from ex1 import TransformCreatureFactory, HealingCreatureFactory
from ex2.strategy import BattleStrategy, NormalStrategy
from ex2.strategy import AggressiveStrategy, DefensiveStrategy
from ex2.strategy import InvalidCreature


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]):
    opponent: list = []
    creatures: list = []
    strategies: list = []

    for creature_type, creature_strategy in opponents:
        creature = creature_type.create_base()
        creatures.append(creature)
        strategies.append(creature_strategy)
        opponent.append(f"({creature.type_of_strategy}+"
                        f"{creature_strategy.strategy})")
    print("[ " + ", ".join(opponent) + " ]")

    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    # for i, j in combinations(range(len(creatures)), 2):
    for i in range(len(creatures)):
        for j in range(i + 1, len(creatures)):
            fighter_1, fighter_2 = creatures[i], creatures[j]
            strategy_1, strategy_2 = strategies[i], strategies[j]

            print("\n* Battle *")
            print(fighter_1.describe())
            print("vs.")
            print(fighter_2.describe())
            print("now fight!")
            print(strategy_1.act(fighter_1))
            print(strategy_2.act(fighter_2))


if __name__ == "__main__":
    factory_1 = FlameFactory()
    factory_2 = AquaFactory()
    factory_3 = TransformCreatureFactory()
    factory_4 = HealingCreatureFactory()

    strategy_1 = NormalStrategy()
    strategy_2 = AggressiveStrategy()
    strategy_3 = DefensiveStrategy()

    print("Tournament 0 (basic)")
    battle([(factory_1, strategy_1), (factory_4, strategy_3)])

    print("\nTournament 1 (error)")
    try:
        battle([(factory_1, strategy_2), (factory_4, strategy_3)])
    except InvalidCreature as exc:
        print(f"{exc}")

    print("\nTournament 2 (multiple)")
    battle([(factory_2, strategy_1), (factory_4, strategy_3),
            (factory_3, strategy_2)])
