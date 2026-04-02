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
        #  Параметры прищельцев
        self.fleet_drop_speed = 15
        self.fleet_direction = 1

        #  Темп ускорения игры
        self.speedup_scale = 1.1
        self.initialize_dinamic_settings()

    def initialize_dinamic_settings(self):
        """Инициализирует настройки, изменяющиейся в ходе игры."""
        self.ship_speed_factor = 0.5
        self.bullet_speed_factor = 1.0
        self.alien_speed_factor = 0.2

        #  fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличивает настройки скорости"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale