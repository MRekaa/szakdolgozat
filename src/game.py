import pygame
from settings import *


class Game:
    def __init__(self, window_size):
        self.display_surface = pygame.display.get_surface()
        self.pos = (PADDING, PADDING)
        self.update_sizes(window_size)

    def update_sizes(self, window_size):
        ghb_w, hb_h, game_w, game_h = compute_sizes(window_size[0], window_size[1])
        self.surface = pygame.Surface((game_w, game_h))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], game_w, game_h)

    def run(self):
        self.surface.fill(WHITE)
        self.display_surface.blit(self.surface, (PADDING, PADDING))

