import random

class Settings():
    """Класс для хранения всех настроек игры"""

    def __init__(self):
        """Инициализирует настройки игры"""
        #  Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (20, 20, 60)
        #  Параметры корабля
        self.ship_limit = 3
        #  Параметры стрельбы
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (0, 255, 150)
        self.bullet_power = 40
        #  Параметры прищельцев
        #self.fleet_drop_speed = 15
        #self.fleet_direction = 1
        self.hp_alien2 = 100
        self.hp_color = (0, 255, 0)
        

        #  Темп роста стоимости пришельцев
        self.score_scale = 1.3
        #  Темп ускорения игры
        self.speedup_scale = 1.04

        #  Настройки кнопок
        self.basic_button_width = 200
        self.basic_button_height = 50
        #  Play
        self.play_button_color = (0, 250, 0)
        self.play_button_xpos = (self.screen_width / 2) - 100
        self.play_button_ypos = (self.screen_height / 2) - 50
        #  Setting
        self.setting_button_color = (0, 0, 250)
        self.setting_button_xpos = (self.screen_width / 2) - 100
        self.setting_button_ypos = (self.screen_height / 2) + 50
        #  Back to the main menu
        self.back_button_color = (0, 0, 250)
        self.back_button_xpos = 50
        self.back_button_ypos = 50
        self.back_button_width = 90
        self.back_button_height = 50
        self.initialize_dinamic_settings()

    def initialize_dinamic_settings(self):
        """Инициализирует настройки, изменяющиейся в ходе игры."""
        self.ship_speed_factor = 0.5
        self.bullet_speed_factor = 1.0
        self.x_min_speed = 0.01
        self.x_max_speed = 0.07
        self.y_min_speed = 0.01
        self.y_max_speed = 0.04
        self.aliens_number = 5
        self.aliens2_number = 1
        #  Подсчет очков
        self.alien_points = 5
        self.alien2_points = 20

        #  fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1


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

        self.alien_points = int(self.alien_points * self.score_scale)