import pygame.font

class Button():

    def __init__(self, ai_game, msg, button_color, xpos, ypos, width, height):
        """Инициализирует атрибуты кнопки"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        #  Назначение размеров и свойств кнопок
        #self.width, self.height = 200, 50
        #self.button_color = (0, 250, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('ISOCPEUR', 48)

        #  Построение объекта rect кнопки и выравнивания по центру экрана
        self.rect = pygame.Rect(xpos, ypos, width, height)
        #self.rect.center = self.screen_rect.center


        #  Сообщение кнопки создается только один раз
        self._prep_msg(msg, button_color)

    def _prep_msg(self, msg, button_color):
        """Преобразует msg  в прямоугольник и выравнивает текст по центру"""
        self.msg_image = self.font.render(msg, True, self.text_color, button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self, button_color):
        #  Отображение пустой кнопки и вывод сообщения
        #self.screen.fill(button_color, self.rect)
        pygame.draw.rect(self.screen, button_color, self.rect, border_radius=20)
        self.screen.blit(self.msg_image, self.msg_image_rect)