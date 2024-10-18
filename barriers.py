import pygame as pg
import sys
from pygame.sprite import Sprite

class Barrier(Sprite):
    pieces = ["bot_left", "top_left", "mid", "top_right", "bot_right"]      # build barrier from bot left to bot right
    images = [pg.image.load(f'images/{piece}.png') for piece in pieces]

    def __init__(self, game, piece_num=0):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings

        self.image = Barrier.images[piece_num % len(Barrier.pieces)]
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def update(self):
        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)

class Barriers():
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.ship = game.ship
        self.aliens = game.aliens
        self.ship_lasers = game.ship.lasers
        self.alien_lasers = game.aliens.lasers
        self.screen_rect = game.screen.get_rect()
        
        self.barrier_group = pg.sprite.Group()
        self.create_barrier()

    def create_piece(self, x, y, piece_num):
        piece = Barrier(self.game, piece_num)
        piece.rect.x, piece.rect.y = x, y
        self.barrier_group.add(piece)

    def reset(self):
        self.barrier_group.empty()
        self.create_barrier()
    
    def create_barrier(self):
        # create the spacing between different pieces
        x = [0, 0, 42, 75, 89]
        y = [0, -30, -30, -30, 2]

        # starting coordinates for the leftmost barrier
        start_x = 86
        start_y = 580
        num_barriers = 4

        while(num_barriers > 0):
            for num in range(0,5):
                self.create_piece(x = start_x + x[num], y = start_y + y[num], piece_num = num)
            
            num_barriers -= 1
            start_x += 300




    def update(self):
        # check for alien lasers to barrier collision
        collisions = pg.sprite.groupcollide(self.aliens.lasers.lasergroup(), self.barrier_group, True, True)
        
        # check for ship lasers to barrier collision
        collisions = pg.sprite.groupcollide(self.ship.lasers.lasergroup(), self.barrier_group, True, True)

        # check for alien to barrier collision
        collisions = pg.sprite.groupcollide(self.aliens.alien_group, self.barrier_group, True, True)

        for piece in self.barrier_group.sprites():
            piece.update()