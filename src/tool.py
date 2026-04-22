import pygame


class Tool:
    def __init__(self, x: int, y: int, image_path: str):
        self.x = x
        self.y = y

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((50, 50))
            self.image.fill((200, 200, 200))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect.topleft)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.rect.move_ip(event.rel)