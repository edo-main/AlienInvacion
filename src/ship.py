import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Класс для управления кораблём"""

    def __init__(self, ai_game):
        """Инициализирует корабль и создаёт его начальную позицию"""
        super().__init__()

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.ai_game = ai_game

        #  Загружаем изображение корабля и получаем прямоугольник
        self.images = {}
        self.suffixes = ['', '_shield']
        self.directions = ['dir', 'right', 'left']

        for direction in self.directions:
            for suffix in self.suffixes:
                key = f"{direction}{suffix}"
                filename = f"assets/images/ship{key}.png"
                self.images[key] = pygame.transform.scale(pygame.image.load(filename).convert_alpha(),(110, 110))

        self.rect = self.images['dir'].get_rect()
        #  Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom
        #  Сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)

        #  Флаг перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляем позицию корабля с учетом флагов"""
        #  Обновляется атрибут x, не rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed_factor

        #  Обновление атрибута rect на основании self.x
        self.rect.x = self.x
        

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.current_image_key = self.get_current_image_key()
        self.image = self.images[self.current_image_key]
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def get_current_image_key(self):
        if self.moving_right:
            direction = 'right'
        elif self.moving_left:
            direction = 'left'
        else:
            direction = 'dir'

        if self.ai_game.shield_bonus_active:
            return f"{direction}_shield"
        else:
            return direction

    # def update_image(self):
    #     self.current_image_key = self.get_current_image_key()
    #     self.image = self.images[self.current_image_key]

