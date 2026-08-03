import pygame
from .button import Button

class SettingsMenu():

    def __init__(self, ai_game):

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        #self.button = ai_game.button



        self.back_button = Button(ai_game, 'Back', self.settings.back_button_color,
                                          self.settings.back_button_xpos,
                                          self.settings.back_button_ypos,
                                          self.settings.back_button_width,
                                          self.settings.back_button_height)
        #self.rect = self.back_button.get_rect()

    def draw_settings_menu(self):
       self.back_button.draw_button(self.settings.back_button_color)