from alchemy.grimoire.light_spellbook import light_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    allowed_ingredients: list[str] = light_spell_allowed_ingredients()

    for ingredient in allowed_ingredients:
        if ingredient in ingredients.lower():
            return f"{ingredients}- VALID"
    return f"{ingredients}- INVALID"
