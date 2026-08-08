import json
import pygame
class Saver():

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats
        self.old_record = self.json_read()['old_record']

        self.record_text_color = (100, 70, 250)
        self.font = pygame.font.SysFont(None, 72)
        self.prep_old_record()


    def json_write(self):
        with open('saves/highscore.json', 'w') as f:
            json.dump(self.new_record_dict, f)

    def json_read(self):
        with open('saves/highscore.json', 'r') as f:
            return json.load(f)

    def save_new_record(self):
        if self.stats.high_score > self.old_record:
            self.new_record_dict = {'old_record' : self.stats.high_score}
            self.old_record = self.stats.high_score
            self.prep_old_record()
            self.json_write()

    def prep_old_record(self):
            """Преобразует рекордный счет в графическое изображение"""
            old_record_str = str(f"Record  {self.old_record}")
            self.old_record_image = self.font.render(old_record_str, True,
                                                     self.record_text_color)
            self.old_record_rect = self.old_record_image.get_rect()
            self.old_record_rect.right = self.screen_rect.right - 20
            self.old_record_rect.top = 110
    def show_old_record(self):
            self.screen.blit(self.old_record_image, self.old_record_rect)