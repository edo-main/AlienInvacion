import random
import pygame
from pygame.sprite import Sprite

class RapidBonus(Sprite):

    def __init__(self, ai_game):

        super().__init__()

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.image = pygame.image.load('assets/images/rapid2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()

        self.rect.x = self.screen_rect.width / 2
        self.rect.y = -100

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.rand_direction = random.randrange(2)
        if self.rand_direction == 0:
            self.direction = -1
        else:
            self.direction = 1
        self.x_speed = random.uniform(0.1, 0.4)
        self.y_speed = random.uniform(0.1, 0.7)

    def update(self):
        self.x += self.x_speed * self.direction
        self.y += self.y_speed
        self.rect.x = self.x
        self.rect.y = self.y
        self.change_direction()
   

    def change_direction(self):
        if self.rect.right > self.screen_rect.right or self.rect.left <= 0:
            self.direction *= -1

    def random_drop_rapid(self):
        get = random.randint(0, 20)
        if get < 2:
            return True

    # def draw_fast_fire(self):
    #     self.screen.blit(self.image, self.rect)
