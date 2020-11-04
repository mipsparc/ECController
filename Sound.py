#encoding: utf-8

import pygame
import time

class Sound:
    def __init__(self):
        pygame.mixer.init(44100, -16, 1, 256)
        self.ding = SoundPlayer(['sound/ding_bell.wav'], 1.0)
        self.door_phases = {
            1 : "door opened",
            2 : "door closing",
            3:  "door closed",
            4:  "door opening"
        }
        self.door_phase = 1
        self.air = SoundPlayer(['sound/air_out.wav'], 5.0)
        self.brake_last_eb = False
        
    def door(self, button_pressed):
        if not pygame.mixer.music.get_busy():
            if self.door_phase == 1 and button_pressed:
                pygame.mixer.music.load('sound/door_close.wav')
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play()
                self.door_phase = 3
            elif self.door_phase == 3 and not button_pressed:
                pygame.mixer.music.load('sound/door_open.wav')
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play()
                self.door_phase = 1

    def horn(self, button_pressed):
        if button_pressed and not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('sound/horn.wav')
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play()
            
    def music_horn(self, button_pressed):
        if button_pressed and not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('sound/music_horn.wav')
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play()
            
    def slow_start(self,button_pressed):
        if button_pressed and not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('sound/slow.wav')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            
    def ding_bell(self, button_pressed):
        if button_pressed:
            self.ding.play()
            
    def air_out(self, brake_knotch):
        if brake_knotch == 9 or brake_knotch == 8:
            self.brake_last_eb = True
        if brake_knotch < 8 and self.brake_last_eb:
            self.brake_last_eb = False
            self.air.play()

class SoundPlayer:
    def __init__(self, paths, duration=False):
        self.sound = []
        self.duration = duration
        self.last_play = time.time()
        for path in paths:
            self.sound.append(pygame.mixer.Sound(path))
            
    def play(self, num=0, loop=False):
        if loop:
            self.sound[num].play(loops=-1)
        elif self.last_play + self.duration < time.time():
            self.last_play = time.time()
            self.sound[num].play()
            
    def stop(self):
        for sound in self.sound:
            sound.stop()
        
    def volume(self, v):
        for s in self.sound:
            s.set_volume(v)
