import pygame

class SearchSystem:
    def __init__(self, reaction_manager, font):
        self.reaction_manager = reaction_manager
        self.font = font
        self.query = ""
        self.suggestions = []
        self.is_active = True 

    def handle_event(self, event):
        if not self.is_active: return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.query = self.query[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.query = ""
            else:
                if event.unicode.isprintable():
                    self.query += event.unicode

            self._update_suggestions()

    def _update_suggestions(self):
        if not self.query:
            self.suggestions = []
            return

        q = self.query.lower()
        results = []

        all_reactions = self.reaction_manager.reactions

        for ingredients, result in all_reactions.items():
            output_list = self._extract_output_names(result)

            match_found = False
            for res_name in output_list:
                if q in res_name.lower():
                    match_found = True
                    break

            if match_found:
                results.append((output_list, list(ingredients)))

        self.suggestions = results

    def _extract_output_names(self, result):
        if isinstance(result, str):
            return [result]
        if isinstance(result, dict):
            raw_result = result.get('result', [])
            if isinstance(raw_result, str):
                return [raw_result]
            return list(raw_result) if isinstance(raw_result, (list, tuple)) else []
        if isinstance(result, (list, tuple)):
            return list(result)
        return []

    def draw(self, surface):
        if not self.query and not self.is_active: return

        x, y = 20, 20
        query_surf = self.font.render(f"Search: {self.query}_", True, (255, 255, 255))
        surface.blit(query_surf, (x, y))

        for i, (res_names, ingr) in enumerate(self.suggestions[:5]):
            res_str = " + ".join(res_names)
            ing_str = " + ".join(ingr)
            recipe_text = f"{ing_str} = {res_str}"

            row_surf = self.font.render(recipe_text, True, (200, 255, 200))
            surface.blit(row_surf, (x, y + 30 + (i * 25)))