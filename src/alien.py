import random
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, sg):
        super().__init__()

        self.screen = sg.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sg.settings

        self.image = pygame.image.load('assets/images/alien.bmp')
        self.image = pygame.transform.scale(self.image, (80, 80))

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        #  Создаем случайные значения для скорости и направления пришельцев
        self.rand_direction = random.randrange(2)
        if self.rand_direction == 0:
            self.direction = -1
        else:
            self.direction = 1
        self.x_speed = random.uniform(self.settings.x_min_speed, self.settings.x_max_speed)
        self.y_speed = random.uniform(self.settings.y_min_speed, self.settings.y_max_speed)

    def check_edges(self):
        """Возвраащет True, если пришелец находится у края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True 

    def update(self):
        """Перемещает пришельца вправо"""
        self.x += self.x_speed * self.direction
        self.rect.x = self.x
        self.y += self.y_speed
        self.rect.y = self.y
        self.change_direction()

    def change_direction(self):
        if self.rect.right > self.screen_rect.right or self.rect.left <= 0:
            self.direction *= -1
