def light_spell_allowed_ingredients() -> list[str]:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    from alchemy.grimoire.light_validator import validate_ingredients

    if "VALID" in validate_ingredients(ingredients):
        return f"Spell recorded: {spell_name} \
            ({validate_ingredients(ingredients)})"
    else:
        return f"Spell rejected: {spell_name} \
            ({validate_ingredients(ingredients)})"
