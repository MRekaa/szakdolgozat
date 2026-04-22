from config import REACTIONS

class Reaction:
    def __init__(self, game):
        self.game = game
        self.reactions = REACTIONS

    def can_react(self, item1, item2):
        pair = frozenset([item1.name, item2.name])
        return pair in self.reactions

    def check(self, item1, item2):
        pair = frozenset([item1.name, item2.name])
        recipe_data = self.reactions.get(pair)

        if recipe_data:
            results_list, display_label = self._extract_results(recipe_data)

            for i, res_name in enumerate(results_list):
                spawn_pos = (item1.rect.centerx + (i * 40), item1.rect.centery)
                self.game.spawn_item(res_name, spawn_pos, "Material", parents=[item1, item2],
                                   display_label=display_label)

            if item1 in self.game.world_items:
                self.game.world_items.remove(item1)
            if item2 in self.game.world_items:
                self.game.world_items.remove(item2)

            return True
        return False

    def _extract_results(self, recipe_data):
        if isinstance(recipe_data, dict):
            results_list = recipe_data.get("result", [])
            display_label = recipe_data.get("equation", "")
        else:
            display_label = None
            results_list = [recipe_data] if isinstance(recipe_data, str) else recipe_data

        return results_list, display_label

    def get_recipe(self, target_name):
        results = []

        for ingredients, result in self.reactions.items():

            if isinstance(result, dict):
                values = result["result"]
            elif isinstance(result, list):
                values = result
            else:
                values = [result]

            if target_name in values:
                results.append(sorted(list(ingredients)))

        return results

    def _matches_result(self, result, target_name):
        if isinstance(result, str):
            return result == target_name
        elif isinstance(result, dict):
            return target_name in result.get("result", [])
        elif isinstance(result, list):
            return target_name in result
        return False