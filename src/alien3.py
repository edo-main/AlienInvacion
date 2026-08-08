import random
import pygame
from pygame.sprite import Sprite

class Alien3(Sprite):

    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.image = pygame.image.load('assets/images/alpix3.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (110, 110))

        self.rect = self.image.get_rect()

        # Создаем полоску хп
        self.hp_width = 100
        self.hp_rect = pygame.Rect(0, 0, self.hp_width, 4)
        self.hp_rect.center = self.rect.center
        self.hp_rect.bottom = self.rect.top - 5
        self.hp = self.settings.hp_alien3  #  Количество хп

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

        self.start_time = 0
        self.next_decision_time = random.randint(1000, 4000)

    def update(self):
        """Перемещает пришельца вправо"""
        self.x += self.x_speed * self.direction
        self.y += self.y_speed
        self.rect.x = self.x
        self.rect.y = self.y
        self.hp_rect.x = self.rect.x
        self.hp_rect.y = self.rect.y
        self.hp_rect = pygame.Rect(0, 0, self.hp_width, 5)
        self.hp_rect.center = self.rect.center
        self.hp_rect.bottom = self.rect.top
        self.change_direction()
        self.decision_change_direction()

    def change_direction(self):
        if self.rect.right > self.screen_rect.right or self.rect.left <= 0:
            self.direction *= -1

    def decision_change_direction(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.start_time >= self.next_decision_time:
            random_decision_change = random.randint(0, 10)
            if random_decision_change < 4:
                self.direction *= -1
            self.start_time = self.current_time

    def draw_alien3(self):  
        pygame.draw.rect(self.screen, self.settings.hp_color, self.hp_rect)