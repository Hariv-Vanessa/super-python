from ex0.factory import CreatureFactory, FlameFactory, AquaFactory


def ft_test_factory(Fac: CreatureFactory) -> None:
    print("\nTesting factory")

    creature_1 = Fac.create_base()
    print(creature_1.describe())
    print(creature_1.attack())

    creature_2 = Fac.create_evolved()
    print(creature_2.describe())
    print(creature_2.attack())


def ft_battle(
        creature_1: CreatureFactory,
        creature_2: CreatureFactory
) -> None:
    print("\nTesting battle")
    fighter_1 = creature_1.create_base()
    fighter_2 = creature_2.create_base()

    print(fighter_1.describe())
    print("vs")
    print(fighter_2.describe())
    print("fight!")
    print(fighter_1.attack())
    print(fighter_2.attack())


if __name__ == "__main__":
    flame = FlameFactory()
    aqua = AquaFactory()

    ft_test_factory(flame)
    ft_test_factory(aqua)
    ft_battle(flame, aqua)
