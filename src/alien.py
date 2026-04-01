import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, sg):
        super().__init__()

        self.screen = sg.screen
        self.settings = sg.settings

        self.image = pygame.image.load('assets/images/alien.bmp')
        self.image = pygame.transform.scale(self.image, (80, 80))

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        """Возвраащет True, если пришелец находится у края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True 

    def update(self):
        """Перемещает пришельца вправо"""
        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        self.rect.x = self.x
