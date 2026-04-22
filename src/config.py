import json

DB_AVAILABLE = True

try:
    from dataBase import DatabaseManager
except Exception as err:
    DatabaseManager = None
    DB_AVAILABLE = False
    print(f"Adatbázis modul betöltése sikertelen: {err}")


def _parse_database_value(value):
    if value is None:
        return None

    if isinstance(value, (list, dict)):
        return value

    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None

        try:
            parsed = json.loads(value)
            return parsed
        except json.JSONDecodeError:
            pass

        if "," in value and not value.startswith("["):
            return [item.strip() for item in value.split(",") if item.strip()]

        return value

    return value


def _get_row_value(row, *candidates):
    for key in candidates:
        if key in row and row[key] is not None:
            return row[key]
    return None


def _load_database_configuration():
    reactions = {}
    materials = []
    tools = []

    if DatabaseManager is None:
        return reactions, materials, tools

    db = DatabaseManager()
    reaction_rows = db.get_all_reactions()
    if reaction_rows:
        for row in reaction_rows:
            item1 = _get_row_value(row, 'item1', 'ingredient1', 'reactant1', 'source1')
            item2 = _get_row_value(row, 'item2', 'ingredient2', 'reactant2', 'source2')
            raw_result = _get_row_value(row, 'result', 'results', 'output')
            equation = _get_row_value(row, 'equation', 'formula', 'equation_text') or ""
            if not item1 or not item2 or raw_result is None:
                continue

            result = _parse_database_value(raw_result)
            if isinstance(result, list):
                entry = {'result': result, 'equation': equation}
            else:
                entry = result

            key = frozenset([item1, item2])
            reactions[key] = entry

    materials = db.get_all_materials()
    tools = db.get_all_tools()

    return reactions, materials, tools


REACTIONS, AVAILABLE_MATERIALS, AVAILABLE_TOOLS = _load_database_configuration()


