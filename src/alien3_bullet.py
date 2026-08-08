from pygame.sprite import Sprite
import pygame

class Alien3Bullet(Sprite):
    def __init__(self, ai_game, x, y):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        self.rect = pygame.Rect(0, 0, 
                               self.settings.alien3_bullet_width,
                               self.settings.alien3_bullet_height)
        self.rect.centerx = x
        self.rect.top = y
        self.y = float(self.rect.y)
    
    def update(self):
        self.y += self.settings.alien3_bullet_speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
            pygame.draw.rect(self.screen, self.settings.alien3_bullet_color, self.rect)
    