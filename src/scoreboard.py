import pygame.font
from pygame.sprite import Group

from src.heart import Heart

class Scoreboard():
    """Класс для вывода игровой информации"""

    def __init__(self, ai_game):
        """Инициализирует атрибуты посчета очков"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        #self.old_record = ai_game.old_record
        #self.saver = ai_game.saver
        
        #  Настройка шрифта для вывода счета
        self.score_text_color = (30, 210, 120)
        self.record_text_color = (100, 70, 250)
        self.level_text_color = (240, 7, 50)
        self.font = pygame.font.SysFont(None, 48)
        self.big_font = pygame.font.SysFont(None, 180)
        #  Подготовка исходного изображения
        self.prep_score()
        self.prep_high_score()
        #self.prep_old_record()
        self.prep_level()
        self.prep_hearts()

        self.image_shield = pygame.image.load('assets/images/shieldpix.png').convert_alpha()
        self.image_shield = pygame.transform.scale(self.image_shield, (50, 50))
        self.rect_shield = self.image_shield.get_rect()
        self.rect_shield.x = 20
        self.rect_shield.y = 200

        self.image_rapid = pygame.image.load('assets/images/rapidpix.png').convert_alpha()
        self.image_rapid = pygame.transform.scale(self.image_rapid, (70, 70))
        self.rect_rapid = self.image_rapid.get_rect()
        self.rect_rapid.x = 12
        self.rect_rapid.y = 120



    def prep_score(self):
        """Преобразует текущий счет в графическое изображение"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True,
                    self.score_text_color)
        
        #  Вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение"""
        high_score = self.stats.high_score
        high_score_str = str(f"Score: {high_score}")
        self.high_score_image = self.big_font.render(high_score_str, True,
                    self.record_text_color)
        
        #  Рекорд выравнивается по центру сверху
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.centery = self.screen_rect.centery

    def  prep_level(self):
        """Преобразует уровень в графическое изображение"""
        level_str = str(f"LeveL {self.stats.level}")
        self.level_image = self.font.render(level_str, True,
                    self.level_text_color)
        
        #  Уровень выводится под текущим счетом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def prep_hearts(self):
        """Сообщает количество оставшихся кораблей"""
        self.hearts = Group()
        for heart_number in range(self.stats.ships_left):
            heart = Heart(self.ai_game)
            heart.image = pygame.transform.scale(heart.image, (40, 40))
            rect = heart.image.get_rect()
            heart.rect.x = 20 + heart_number * rect.width
            heart.rect.y = 20
            self.hearts.add(heart)

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Выводит счет, рекорд, уровень и количество жизней на экран"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.hearts.draw(self.screen)

    def show_rapid_bonus(self):
        self.screen.blit(self.image_rapid, self.rect_rapid)

    def show_shield_bonus(self):
        self.screen.blit(self.image_shield, self.rect_shield)

    def show_record(self):
        self.screen.blit(self.high_score_image, self.high_score_rect)

    # def show_old_record(self):
    #     self.screen.blit(self.old_record_image, self.old_record_rect)
