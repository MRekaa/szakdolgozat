import pygame
from sys import exit
from game import Game
from reaction import Reaction
from itemOnBoard import ItemOnBoard
from settings import *
from HB.materialsH import MaterialsH
from HB.toolsH import ToolsH
from searchSystem import SearchSystem
from trash import Trash

class EventHandler: 
    def __init__(self, main):
        self.main = main

    def handle_resize(self, event):
        old_size = (self.main.screen_width, self.main.screen_height)
        new_w, new_h = event.w, event.h
        self.main.screen_width, self.main.screen_height = new_w, new_h
        self.main.display_surface = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)

        self.main.game.update_sizes((new_w, new_h))
        for hotbar in self.main.hotbars.values():
            hotbar.update_sizes((new_w, new_h))

        for item in self.main.world_items:
            item.update_position_ratio(old_size, (new_w, new_h))
            item.rect.clamp_ip(self.main.game.rect)

        trash_pos = (new_w - 2.5 * PADDING, 2.5 * PADDING)
        self.main.trash.rect.center = trash_pos

    def handle_mouse_down(self, event):
        active_hotbar = self.main.hotbars[self.main.active_hotbar]
        
        self.main.dragging_world_item = None
        for item in reversed(self.main.world_items):
            if item.rect.collidepoint(event.pos):
                self.main.dragging_world_item = item
                break

        if self.main.dragging_world_item is None:
            if self._check_tab_rect(active_hotbar, active_hotbar.tab_materials_rect, event.pos):
                self.main.active_hotbar = 'materials'
                return
            if self._check_tab_rect(active_hotbar, active_hotbar.tab_tools_rect, event.pos):
                self.main.active_hotbar = 'tools'
                return
            
            active_hotbar.mouse_down(event.pos)

    def _check_tab_rect(self, hotbar, tab_rect, pos):
        rect = tab_rect.copy()
        rect.x += hotbar.rect.x
        rect.y += hotbar.rect.y
        return rect.collidepoint(pos)

    def handle_mouse_motion(self, event):
        if self.main.dragging_world_item:
            self.main.trash.check_hover(event.pos)
        else:
            self.main.trash.is_hovered = False

    def handle_mouse_up(self, event):
        if self.main.dragging_world_item is not None:
            if self.main.trash.rect.collidepoint(event.pos):
                self.main.trash.delete_item(self.main.dragging_world_item, self.main.world_items)
            else:
                self.main._check_reactions(self.main.dragging_world_item)
            self.main.dragging_world_item = None
            self.main.trash.is_hovered = False
        else:
            self.main.hotbars[self.main.active_hotbar].mouse_up(event.pos)

    def process_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.VIDEORESIZE:
            self.handle_resize(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_mouse_down(event)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.handle_mouse_up(event)


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('Labor')

        self.screen_width, self.screen_height = self.display_surface.get_size()
        self.game = Game((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.reaction = Reaction(self)
        self.event_handler = EventHandler(self)

        self.font = pygame.font.SysFont('Times New Roman', 22)
        self.search_system = SearchSystem(self.reaction, self.font)

        self.hotbars = {
            'materials': MaterialsH((WINDOW_WIDTH, WINDOW_HEIGHT), self),
            'tools': ToolsH((WINDOW_WIDTH, WINDOW_HEIGHT), self)
        }
        self.active_hotbar = 'materials'

        self.world_items = []
        self.dragging_world_item = None

        self.trash = Trash(TRASH_POS, (self.screen_width, self.screen_height))

    def spawn_item(self, name, position, item_type, parents=None, display_label=None):
        item = ItemOnBoard(name, position, item_type, parents=parents, display_label=display_label)
        self.world_items.append(item)
        return item

    def _check_reactions(self, dropped_item):
        for item in self.world_items:
            if item != dropped_item:
                distance = pygame.math.Vector2(dropped_item.rect.center).distance_to(item.rect.center)
                if distance < REACTION_DISTANCE:
                    if self.reaction.check(dropped_item, item):
                        break

    def _update_dragging_item(self, mouse_pos):
        if self.dragging_world_item is None:
            return

        half_w = self.dragging_world_item.rect.width // 2
        half_h = self.dragging_world_item.rect.height // 2

        left_limit = self.game.rect.left + half_w
        right_limit = self.game.rect.right - half_w
        top_limit = self.game.rect.top + half_h
        bottom_limit = self.game.rect.bottom - half_h

        new_x = max(left_limit, min(mouse_pos[0], right_limit))
        new_y = max(top_limit, min(mouse_pos[1], bottom_limit))

        self.dragging_world_item.rect.center = (new_x, new_y)

    def _draw(self):
        for item in self.world_items:
            item.draw(self.display_surface)

        active_hotbar = self.hotbars[self.active_hotbar]
        active_hotbar.run()
        
        for hotbar in self.hotbars.values():
            hotbar.draw_tabs_on_display()
        self.search_system.draw(self.display_surface)

        for item in self.world_items:
            if item.rect.collidepoint(pygame.mouse.get_pos()):
                item.draw_tooltip(self.display_surface, self)
                break
        self.trash.draw(self.display_surface)

    def run(self):
        while True:
            self.display_surface.fill(LIGHT_BLUE)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                self.search_system.handle_event(event)
                self.event_handler.process_event(event)

            self.game.run()
            self._update_dragging_item(mouse_pos)
            self._draw()

            pygame.display.update()

if __name__ == '__main__':
    main = Main()
    main.run()
