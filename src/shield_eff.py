import random
import pygame
from pygame.sprite import Sprite

class ShieldEff(Sprite):

    def __init__(self, ai_game, x, y):

        super().__init__()

        self.screen = ai_game.screen

        self.images = []
        for num in range(1, 4):
            image = pygame.image.load(f"assets/images/shld{num}.png").convert_alpha()
            image = pygame.transform.scale(image, (100, 100))
            #image.set_alpha(200)
            self.images.append(image)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0



    def update(self):
        explosion_speed = 30
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()