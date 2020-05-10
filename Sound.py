#encoding: utf-8

import pygame

class Sound:
    def __init__(self):
        pygame.mixer.init(44100, -16, 1, 256)
        pygame.mixer.music.load('music_horn.wav')
        pygame.mixer.music.set_volume(1.0)

    def horn(self, button_pressed):
        if button_pressed and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
