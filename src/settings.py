import random
import pygame

class Settings():
    """Класс для хранения всех настроек игры"""

    def __init__(self):
        """Инициализирует настройки игры"""
        #  Параметры экрана
        self.screen_width = 1500
        self.screen_height = 900
        self.bg_color = (20, 20, 60)
        self.bg_image = pygame.image.load('assets/images/bg1.jpg')
        self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))
        self.bgy = 0
        self.bg_image_next = pygame.image.load('assets/images/bg1.jpg')
        self.bg_image_next = pygame.transform.scale(self.bg_image_next, (self.screen_width, self.screen_height))
        #  Параметры корабля
        self.ship_limit = 3
        #  Параметры стрельбы
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (0, 255, 150)
        self.bullet_power = 40
        self.fire_delay = 600
        self.last_shot_time = 0
        #  Параметры прищельцев
        self.hp_alien2 = 100
        self.hp_color = (0, 255, 0)
        

        #  Темп роста стоимости пришельцев
        self.score_scale = 1.3
        #  Темп ускорения игры
        self.speedup_scale = 1.04

        #  Настройки кнопок
        self.basic_button_width = 320
        self.basic_button_height = 70
        #  Play
        self.play_button_color = (0, 150, 0)
        self.play_button_xpos = (self.screen_width / 2) - 160
        self.play_button_ypos = (self.screen_height / 2) - 50
        #  Setting
        self.setting_button_color = (0, 0, 150)
        self.setting_button_xpos = (self.screen_width / 2) - 160
        self.setting_button_ypos = (self.screen_height / 2) + 50
        #  Continue
        self.continue_button_color = (100, 60, 250)
        self.continue_button_xpos = (self.screen_width / 2) - 190
        self.continue_button_ypos = (self.screen_height / 2) - 200



        #  Back to the main menu
        self.back_button_color = (60, 60, 180)
        self.back_button_xpos = 50
        self.back_button_ypos = 50
        self.back_button_width = 170
        self.back_button_height = 60
        self.initialize_dinamic_settings()

    def initialize_dinamic_settings(self):
        """Инициализирует настройки, изменяющиейся в ходе игры."""
        self.ship_speed_factor = 0.5
        self.bullet_speed_factor = 1.0
        self.x_min_speed = 0.03
        self.x_max_speed = 0.09
        self.y_min_speed = 0.03
        self.y_max_speed = 0.09
        self.aliens_number = 10
        self.aliens2_number = 2
        #  Подсчет очков
        self.alien_points = 5
        self.alien2_points = 20

        #  fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1

        self.bg_speed = 0.1


    def increase_speed(self):
        """Увеличивает настройки скорости и стоимости пришельцев"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.x_min_speed *= self.speedup_scale
        self.x_max_speed *= self.speedup_scale
        self.y_min_speed *= self.speedup_scale
        self.y_max_speed *= self.speedup_scale
        self.aliens_number += 1
        self.aliens2_number += 1

        self.bg_speed += 0.05

        self.alien_points = int(self.alien_points * self.score_scale)
        self.alien2_points = int(self.alien2_points * self.score_scale)