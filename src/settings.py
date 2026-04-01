class Settings():
    """Класс для хранения всех настроек игры"""

    def __init__(self):
        """Инициализирует настройки игры"""
        #  Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (20, 20, 60)
        #  Параметры корабля
        self.ship_speed = 0.8
        self.ship_limit = 3
        #  Параметры стрельбы
        self.bullet_speed = 1
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (0, 255, 150)
        #  Параметры прищельцев
        self.alien_speed = 0.2
        self.fleet_drop_speed = 20
        self.fleet_direction = 1