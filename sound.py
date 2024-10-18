import pygame as pg
from pygame import mixer 
import time


class Sound:
    def __init__(self):
        mixer.init() 
        self.phaser_sound = mixer.Sound("sounds/ship_laser.wav")
        self.pop_sound = mixer.Sound("sounds/pop.wav")
        self.alien_laser = mixer.Sound("sounds/alien_laser.wav")
        self.ufo_enter = mixer.Sound("sounds/ufo_enter.wav")
        self.game_over = mixer.Sound("sounds/game_over.wav")
        self.volume = 0.1
        self.set_volume(self.volume)        
    
    def set_volume(self, volume=0.3):
        mixer.music.set_volume(2 * volume) 
        self.phaser_sound.set_volume(3 * volume)
        self.pop_sound.set_volume(2 * volume)
        self.alien_laser.set_volume(1.5 * volume)
        self.ufo_enter.set_volume(4 * volume)
        self.game_over.set_volume(5 * volume)

    def play_music(self, filename): 
        self.stop_music()
        mixer.music.load(filename)
        mixer.music.play(loops=-1)  
 
    def pause_music(self): 
        mixer.music.pause()

    def unpause_music(self):
        mixer.music.unpause()      

    def stop_music(self): 
        mixer.music.stop() 
 
    def play_phaser(self): 
        mixer.Sound.play(self.phaser_sound) 

    def play_pop(self):
        mixer.Sound.play(self.pop_sound)

    def play_ufo_enter(self):
        mixer.Sound.play(self.ufo_enter)

    def play_alien_laser(self):
        mixer.Sound.play(self.alien_laser)

    def play_game_over(self):
        mixer.pause()
        self.stop_music()
        mixer.Sound.play(self.game_over)
        time.sleep(2.5)