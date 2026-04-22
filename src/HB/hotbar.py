import pygame
from settings import *


class Hotbar:
    def __init__(self, window_size, game):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont(None, 24)

        self.offset = 0
        self.dragging_item = None
        self.drag_offset = (0, 0)
        self.drag_surface = None
        self.slot_rects = []
        self.slot_size = 94
        self.slot_padding = 10

        self.tab_materials_rect = pygame.Rect(0, 0, 0, 0)
        self.tab_tools_rect = pygame.Rect(0, 0, 0, 0)
        self.active_tab = "Materials" 
        self.update_sizes(window_size)

    def update_sizes(self, window_size):
        HOTBAR_WIDTH = window_size[0] - 40
        self.hotbar_height = int(window_size[1] * 0.2)
        self.surface = pygame.Surface((HOTBAR_WIDTH, self.hotbar_height))
        self.rect = self.surface.get_rect(midbottom=(window_size[0]//2, window_size[1] - 20))

        self.slot_size = min(94, self.hotbar_height - 20)
        self.slot_padding = 10
        self.visible_slots = max(1, (HOTBAR_WIDTH - 120) // (self.slot_size + self.slot_padding))

        self.tab_materials_rect.width = int(HOTBAR_WIDTH * 0.15)
        self.tab_materials_rect.height = 30
        self.tab_materials_rect.x = int(HOTBAR_WIDTH * 0.05)
        self.tab_materials_rect.y = -self.tab_materials_rect.height - 10

        self.tab_tools_rect.width = int(HOTBAR_WIDTH * 0.15)
        self.tab_tools_rect.height = 30
        self.tab_tools_rect.x = self.tab_materials_rect.right + 20
        self.tab_tools_rect.y = self.tab_materials_rect.y

        self.left_button = pygame.Rect(10, self.hotbar_height // 2 - 20, 40, 40)
        self.right_button = pygame.Rect(HOTBAR_WIDTH - 50, self.hotbar_height // 2 - 20, 40, 40)

    def draw_slots(self):
        self.slot_rects = []
        for i in range(self.visible_slots):
            x = 60 + i * (self.slot_size + self.slot_padding)
            y = (self.hotbar_height - self.slot_size) // 2
            rect = pygame.Rect(x, y, self.slot_size, self.slot_size)
            self.slot_rects.append(rect)
            pygame.draw.rect(self.surface, (200, 200, 200), rect)

            item_index = self.offset + i
            if item_index < len(self.items):
                text = self.font.render(self.items[item_index], True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                self.surface.blit(text, text_rect)

    def _draw_tab(self, surface, tab_rect, label, is_active=False):
        color = (180, 180, 180)
        pygame.draw.rect(surface, color, tab_rect)
        text = self.font.render(label, True, (0, 0, 0))
        surface.blit(text, text.get_rect(center=tab_rect.center))

    def draw_tabs(self):
        self._draw_tab(self.surface, self.tab_materials_rect, "Materials")
        self._draw_tab(self.surface, self.tab_tools_rect, "Tools")

    def draw_tabs_on_display(self):
        mat_rect = self.tab_materials_rect.copy()
        tool_rect = self.tab_tools_rect.copy()

        mat_rect.x += self.rect.x
        mat_rect.y += self.rect.y
        tool_rect.x += self.rect.x
        tool_rect.y += self.rect.y

        self._draw_tab(self.display_surface, mat_rect, "Materials", self.active_tab == "Materials")
        self._draw_tab(self.display_surface, tool_rect, "Tools", self.active_tab == "Tools")

    def draw_scroll_buttons(self):
        pygame.draw.rect(self.surface, (150, 150, 150), self.left_button)
        pygame.draw.rect(self.surface, (150, 150, 150), self.right_button)

        left_text = self.font.render("<", True, (0, 0, 0))
        right_text = self.font.render(">", True, (0, 0, 0))

        self.surface.blit(left_text, left_text.get_rect(center=self.left_button.center))
        self.surface.blit(right_text, right_text.get_rect(center=self.right_button.center))

    def _handle_scroll_button_click(self, local_pos):
        if self.left_button.collidepoint(local_pos) and self.offset > 0:
            self.offset -= 1
        elif self.right_button.collidepoint(local_pos) and \
                self.offset + self.visible_slots < len(self.items):
            self.offset += 1

    def click(self, mouse_pos):
        local_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)
        self._handle_scroll_button_click(local_pos)

    def mouse_down(self, mouse_pos):
        local_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)

        for i, rect in enumerate(self.slot_rects):
            item_index = self.offset + i
            if item_index < len(self.items) and rect.collidepoint(local_pos):
                self.dragging_item = item_index
                self.drag_surface = self.font.render(
                    self.items[item_index], True, (0, 0, 0))
                self.drag_offset = (
                    rect.centerx - local_pos[0],
                    rect.centery - local_pos[1])
                return

        self._handle_scroll_button_click(local_pos)

    def mouse_up(self, mouse_pos):
        if self.dragging_item is not None:
            dropped_on_slot = False
            local_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)

            for rect in self.slot_rects:
                if rect.collidepoint(local_pos):
                    dropped_on_slot = True
                    break

            if not dropped_on_slot:
                item_name = self.items[self.dragging_item]
                self.game.spawn_item(item_name, mouse_pos, self.type)

            self.dragging_item = None
            self.drag_surface = None

    def run(self):
        self.surface.fill(GRAY)
        self.draw_slots()
        self.draw_scroll_buttons()
        self.draw_tabs()

        if self.dragging_item is not None and self.drag_surface is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.display_surface.blit(
                self.drag_surface,
                (mouse_x - self.drag_offset[0],
                 mouse_y - self.drag_offset[1])
            )

        self.display_surface.blit(self.surface, self.rect)