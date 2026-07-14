from alchemy.grimoire.dark_validator import validate_ingredients


def dark_spell_allowed_ingredients() -> list[str]:
    return ["bats", "frogs", "arsenic", "eyeball"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:

    if "VALID" in validate_ingredients(ingredients):
        return f"Spell recorded: {spell_name} \
            ({validate_ingredients(ingredients)})"
    else:
        return f"Spell rejected: {spell_name} \
            ({validate_ingredients(ingredients)})"
