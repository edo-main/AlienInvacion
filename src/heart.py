import random
import pygame
from pygame.sprite import Sprite

class Heart(Sprite):

    def __init__(self, ai_game):

        super().__init__()

        self.screen = ai_game.screen

        self.image = pygame.image.load('assets/images/heartpix32.png').convert_alpha()
        self.rect = self.image.get_rect()


    def draw_heart(self):
        self.screen.blit(self.image, self.rect)
        