import pygame
import os
from settings import ITEM_IMAGE_SIZE, ITEM_FONT, ITEM_TYPE_MATERIAL, ITEM_TYPE_TOOL


class ItemOnBoard:
    def __init__(self, name, position, item_type, parents=None, display_label=None):
        self.name = name
        self.display_label = display_label
        self.item_type = item_type
        self.position = position
        self.font = pygame.font.SysFont(*ITEM_FONT)

        self.parents = parents or []
        self.children = []
        self._initialize_history()

        self.image = self._load_image()
        self.rect = self.image.get_rect(center=position)

    def _initialize_history(self):
        if not self.parents:
            self.history = [self.name]
        else:
            self.history = []
            for parent in self.parents:
                self.history.extend(parent.history)
                parent.children.append(self)

    def _load_image(self):
        path = self._get_image_path()

        if path and os.path.exists(path):
            try:
                image = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(image, ITEM_IMAGE_SIZE)
            except pygame.error:
                pass

        return self.font.render(self.name, True, (0, 0, 0))

    def _get_image_path(self):
        if self.item_type == ITEM_TYPE_MATERIAL:
            return f"img/materials/{self.name}.png"
        elif self.item_type == ITEM_TYPE_TOOL:
            return f"img/tools/{self.name}.png"
        return None

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
        if self.parents and self.history:
            history_text = " + ".join(self.history)
            text_surf = self.font.render(history_text, True, (255, 0, 0))
            text_rect = text_surf.get_rect(midbottom=(self.rect.centerx, self.rect.top - 5))
            surface.blit(text_surf, text_rect)

    def update_position(self, pos):
        self.rect.center = pos

    def update_position_ratio(self, old_size, new_size):
        ratio_x = new_size[0] / old_size[0]
        ratio_y = new_size[1] / old_size[1]
        new_x = int(self.rect.centerx * ratio_x)
        new_y = int(self.rect.centery * ratio_y)
        self.rect.center = (new_x, new_y)

    def draw_tooltip(self, surface, game):
        mouse_pos = pygame.mouse.get_pos()
        if not self.rect.collidepoint(mouse_pos):
            return

        suggestion = self._find_reaction_suggestion(game)
        lines = self._build_tooltip_lines(suggestion)

        self._render_tooltip(surface, mouse_pos, lines)

    def _find_reaction_suggestion(self, game):
        for other in game.world_items:
            if other == self:
                continue
            if game.reaction.can_react(self, other):
                return other.name
        return None

    def _build_tooltip_lines(self, suggestion):
        lines = [
            f"Name: {self.name}",
            f"Type: {self.item_type}",
            f"History: {' + '.join(self.history)}",
            f"Equation: {self.display_label}",
            "----",
        ]

        if suggestion:
            lines.append(f"Try with: {suggestion}")
        else:
            lines.append("No known combination")

        return lines

    def _render_tooltip(self, surface, mouse_pos, lines):
        padding = 5
        texts = [self.font.render(line, True, (255, 255, 255)) for line in lines]

        width = max(t.get_width() for t in texts) + padding * 2
        height = sum(t.get_height() for t in texts) + padding * 2

        tooltip_rect = pygame.Rect(mouse_pos[0] + 10, mouse_pos[1] + 10, width, height)

        pygame.draw.rect(surface, (0, 0, 0), tooltip_rect)
        pygame.draw.rect(surface, (255, 255, 255), tooltip_rect, 2)

        y_offset = tooltip_rect.y + padding
        for text in texts:
            surface.blit(text, (tooltip_rect.x + padding, y_offset))
            y_offset += text.get_height()