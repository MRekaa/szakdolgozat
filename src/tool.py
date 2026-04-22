import settings
import pygame


class Tool:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        try:
            self.image = pygame.image.load(image_path)
        except pygame.error:
            self.image = pygame.Surface((50, 50))
            self.image.fill((200, 200, 200))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False

    def clone(self, x, y):
        return Tool(x, y + settings.HOTBAR_Y, self._get_image_path())

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.rect.move_ip(event.rel)