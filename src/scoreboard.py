import pygame.font
from pygame.sprite import Group

from src.ship import Ship

class Scoreboard():
    """Класс для вывода игровой информации"""

    def __init__(self, ai_game):
        """Инициализирует атрибуты посчета очков"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #  Настройка шрифта для вывода счета
        self.text_color = (30, 210, 120)
        self.font = pygame.font.SysFont(None, 48)
        #  Подготовка исходного изображения
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True,
                    self.text_color, self.settings.bg_color)
        
        #  Вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Выводит счет, рекорд, уровень и количество жизней на экран"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение"""
        high_score = self.stats.high_score
        high_score_str = str(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                    self.text_color, self.settings.bg_color)
        
        #  Рекорд выравнивается по центру сверху
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def  prep_level(self):
        """Преобразует уровень в графическое изображение"""
        level_str = str(f"LeveL {self.stats.level}")
        self.level_image = self.font.render(level_str, True,
                    (240, 7, 50), self.settings.bg_color)
        
        #  Уровень выводится под текущим счетом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Сообщает количество оставшихся кораблей"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.image = pygame.transform.scale(ship.image, (50, 50))
            rect = ship.image.get_rect()
            ship.rect.x = 20 + ship_number * rect.width
            ship.rect.y = 20
            self.ships.add(ship)

