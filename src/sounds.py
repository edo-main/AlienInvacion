import random
from playsound3 import playsound

class Sounds:
    def __init__(self):
        self.music = 1

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