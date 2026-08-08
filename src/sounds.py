import random
from playsound3 import playsound

class Sounds:
    def __init__(self, ai_game):
        self.music = 1
        self.ai_game = ai_game

        self.shield_sound = None
        self.rapid_sound = None

    def fire(self):
        var_sound_shot = random.randrange(2)
        if var_sound_shot == 1:             
            playsound(r"assets\sounds\shot1.mp3", block=False)
        else:
            playsound(r"assets\sounds\shot2.mp3", block=False)

    def destruction(self):
        var_sound_destruction = random.randrange(5)
        if var_sound_destruction == 1:             
            playsound(r"assets\sounds\destruction1.mp3", block=False)
        elif var_sound_destruction == 2:
            playsound(r"assets\sounds\destruction2.mp3", block=False)
        elif var_sound_destruction == 3:
            playsound(r"assets\sounds\destruction3.mp3", block=False)
        elif var_sound_destruction == 4:
            playsound(r"assets\sounds\destruction4.mp3", block=False)
        else:
            playsound(r"assets\sounds\destruction5.mp3", block=False)

    def ship_hit(self):
        playsound(r"assets\sounds\ship_hit1.mp3", block=False)

    def button(self):
        playsound(r"assets\sounds\button1.mp3", block=False)

    def shield(self, bool):
        if bool:
            self.shield_sound = playsound(r"assets\sounds\shield.mp3", block=False)
        else:
            if self.shield_sound is not None:
                self.shield_sound.stop()

    def rapid(self, bool):
        if bool:
            self.rapid_sound = playsound(r"assets\sounds\rapid.mp3", block=False)
        else:
            if self.rapid_sound is not None:
                self.rapid_sound.stop()

    def alien3fire(self):
        playsound(r"assets\sounds\alien3fire.mp3", block=False)