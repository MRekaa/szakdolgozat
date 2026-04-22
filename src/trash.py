import pygame
from settings import TRASH_SIZE

class Trash:
    def __init__(self, position, screen_size,image_closed=None, image_open=None):
        self.name = "Trash"
        self.width = TRASH_SIZE
        self.height = TRASH_SIZE
        self.position = position
        self.is_hovered = False

        closed_raw = pygame.image.load("img/tools/trashClosed.png").convert_alpha()
        self.image_closed = pygame.transform.scale(closed_raw, (self.width, self.height))

        open_raw = pygame.image.load("img/tools/trashOpen.png").convert_alpha()
        self.image_open = pygame.transform.scale(open_raw, (self.width, self.height))

        self.rect = self.image_closed.get_rect(center=self.position)

    def draw(self, surface):
        current_img = self.image_open if self.is_hovered else self.image_closed

        surface.blit(current_img, self.rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def delete_item(self, item, world_items):
        if item in world_items:
            world_items.remove(item)
            return True
        return False
