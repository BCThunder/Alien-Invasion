import pygame as pg
from pygame.sprite import Sprite
from vector import Vector 
from random import randint
from timer import Timer

class UFO_SPRITE(Sprite):
    ufo_image = [pg.transform.scale(pg.image.load('images/ufo.png'), (100, 64))]
    boom600 = ['1000boom1', '1000boom2', '1000boom3', '1000boom4', '1000boom5', '1000boom6']
    b600_imgs = [pg.transform.scale(pg.image.load(f'images/booms/{str(name)}.png'), (96, 96)) for name in boom600]
    points = 1000

    def __init__(self, game, v=Vector(x=1)):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.sound = game.sound
        self.ship = game.ship

        self.image = UFO_SPRITE.ufo_image[0]
        # self.ufo_image = pg.transform.scale(pg.image.load('images/ufo.png'), (100, 64))
        self.regtimer = Timer(UFO_SPRITE.ufo_image, start_index=0, delta=20)
        self.explosiontimer = Timer(UFO_SPRITE.b600_imgs, start_index = 0, delta=6, looponce=True)
        self.timer = self.regtimer
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.width
        self.rect.y = self.rect.height
        self.v = v

        self.x = float(self.rect.x)
        self.is_dying = False

    def get_ufo_data(self): return self.ufo_image[0]

    def draw(self):
        # if dying:
        #     self.image = self.timer.current_image()
        self.image = self.timer.current_image()
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += self.v.x * self.settings.ufo_speed
        self.rect.x = self.x
        self.draw()

class UFO():
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        self.sb = game.sb
        self.sound = game.sound
        self.v = Vector(self.settings.ufo_speed, 0)
        self.ship = game.ship
        
        self.exists = False
        self.alive_ufo = pg.sprite.Group()
        self.dying_ufo = pg.sprite.Group()
        
    def create_ufo(self):
        ufo = UFO_SPRITE(self.game)
        self.exists = True
        self.alive_ufo.add(ufo)
        
    """ def hit(self):
        self.sound.play_pop()
        # self.ufo.kill()
        self.exists = False
        self.is_dying = True """

    def check_edge(self):
        for ufo in self.alive_ufo:
            if ufo.rect.left >= self.screen_rect.right:
                ufo.kill()
                self.exists = False

    def reset(self):
        self.alive_ufo.empty()
        self.dying_ufo.empty()
        self.exists = False

    def kill_ufo(self):
        self.ufo.kill()
        self.exists = False

    def update(self):
        n = randint(0,10000)

        if n <= self.settings.ufo_spawn_chance and self.exists is False:
            self.create_ufo()
            self.sound.play_ufo_enter()
        elif self.exists:
            for ufo in self.alive_ufo.sprites():
                ufo.update()
                self.check_edge()

        collisions = pg.sprite.groupcollide(self.alive_ufo, self.ship.lasers.lasergroup(), True, True)
        if len(collisions) > 0:
            self.sound.play_pop()
            self.stats.score += UFO_SPRITE.points

            if ufo.is_dying is False:
                ufo.is_dying = True
                ufo.timer = ufo.explosiontimer
                self.dying_ufo.add(ufo)

            self.sb.prep_score()
            self.sb.check_high_score()

        for ufo in self.dying_ufo.sprites():
            if ufo.timer.current_image() == 0:
                ufo.kill()
                self.exists = False
            else:
                ufo.draw()

        
        