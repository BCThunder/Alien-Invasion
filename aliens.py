import pygame as pg
import sys
from pygame.sprite import Sprite
from vector import Vector 
from random import randint
from lasers import Lasers
from timer import Timer
from timer import TimerDict
import time

class Alien(Sprite):
  alien_names = ['bunny', 'pig', 'stalk_eyes', 'w_heart', 'w_pigtails', 'wild_tentacles']
  points = [10, 25, 300, 35, 100, 600]
  images = [pg.image.load(f'images/alien_{name}.png') for name in alien_names] 
  boom10 = ['10boom1', '10boom2', '10boom3', '10boom4', '10boom5', '10boom6']
  b10_imgs = [pg.image.load(f'images/booms/{str(name)}.png') for name in boom10]
  boom25 = ['25boom1', '25boom2', '25boom3', '25boom4', '25boom5', '25boom6']
  b25_imgs = [pg.image.load(f'images/booms/{str(name)}.png') for name in boom25]
  boom35 = ['35boom1', '35boom2', '35boom3', '35boom4', '35boom5', '35boom6']
  b35_imgs = [pg.image.load(f'images/booms/{str(name)}.png') for name in boom35]
  boom100 = ['100boom1', '100boom2', '100boom3', '100boom4', '100boom5', '100boom6']
  b100_imgs = [pg.image.load(f'images/booms/{str(name)}.png') for name in boom100]
  boom300 = ['300boom1', '300boom2', '300boom3', '300boom4', '300boom5', '300boom6']
  b300_imgs = [pg.image.load(f'images/booms/{str(name)}.png') for name in boom300]
  boom600 = ['600boom1', '600boom2', '600boom3', '600boom4', '600boom5', '600boom6']
  b600_imgs = [pg.image.load(f'images/booms/{str(name)}.png') for name in boom600]
  booms = {"boom10" : b10_imgs, "boom25" : b25_imgs, "boom35" : b35_imgs, "boom100" : b100_imgs, "boom300" : b300_imgs, "boom600" : b600_imgs}
  # nameslen = len(names)
  # choices = [randint(0, nameslen) for _ in range(nameslen)]

  li = [x * x for x in range(1, 11)]

  def __init__(self, game, row, alien_no):
    super().__init__()
    self.game = game 
    self.screen = game.screen
    self.screen_rect = self.screen.get_rect()
    self.settings = game.settings

    self.regtimer = Timer(Alien.images, start_index=randint(0, len(Alien.images) - 1), delta=20)
    self.explosiontimer = TimerDict(Alien.booms, start_key = "boom10", delta=6, looponce=True)
    self.timer = self.regtimer

    self.image = Alien.images[row % len(Alien.alien_names)]
    self.alien_no = alien_no
    # self.image = Alien.images[randint(0, 5)]
    # self.image = Alien.images[Alien.choices[row % len(Alien.names)]]
    self.rect = self.image.get_rect()

    self.rect.x = self.rect.width
    self.rect.y = self.rect.height

    self.x = float(self.rect.x)
    self.isdying = False
    self.reallydead = False 

  def laser_offscreen(self, rect): return rect.bottom > self.screen_rect.bottom  

  def laser_start_rect(self):
    rect = self.rect
    rect.midbottom = self.rect.midbottom
    return rect.copy()

  def fire(self, lasers):
    # print(f'Alien {self.alien_no} firing laser')
    lasers.add(owner=self)

  def check_edges(self):
    r = self.rect 
    sr = self.screen_rect
    return r.right >= sr.right or r.left < 0
  
  def check_bottom(self): return self.rect.bottom >= self.screen_rect.bottom 

  def get_alien_data(self): return self.images, self.points
  
  def update(self, v, delta_y):
    self.x += v.x
    self.rect.x = self.x
    self.rect.y += delta_y
    self.draw()

  def draw(self): 
    self.image = self.timer.current_image()
    self.screen.blit(self.image, self.rect)


class Aliens():
  laser_image_files = [f'images/alien_laser_0{x}.png' for x in range(2)]
  laser_images = [pg.transform.scale(pg.image.load(x), (50, 50)) for x in laser_image_files]

  def __init__(self, game):
    self.game = game
    self.screen = game.screen
    self.settings = game.settings 
    self.stats = game.stats
    self.sb = game.sb
    self.sound = game.sound
    self.aliens_created = 0
    self.v = Vector(self.settings.alien_speed, 0)
    self.laser_timer = Timer(image_list=Aliens.laser_images, delta=10)
    self.lasers = Lasers(game=game, v=Vector(0, 1) * self.settings.laser_speed, 
                         timer=self.laser_timer, owner=self)

    self.alien_group = pg.sprite.Group()
    self.dying_aliens = pg.sprite.Group()
    self.ship = game.ship
    self.alien_firing_now = 0
    self.fire_every_counter = 0
    self.create_fleet()

  def create_alien(self, x, y, row, alien_no):
      alien = Alien(self.game, row, alien_no)
      alien.x = x
      alien.rect.x, alien.rect.y = x, y
      self.alien_group.add(alien)
      
  def empty(self): self.alien_group.empty()

  def reset(self):
    self.alien_group.empty()
    self.dying_aliens.empty()
    self.lasers.empty()
    self.create_fleet() 
  
  def create_fleet(self):
    self.fire_every_counter = 0
    alien = Alien(self.game, row=0, alien_no=-1)
    alien_width, alien_height = alien.rect.size 

    x, y, row = alien_width, alien_height+64, 0
    self.aliens_created = 0

    """self.settings.screen_height - 3 * alien_height"""
    while y < (400): 
      while x < (self.settings.screen_width - 2 * alien_width):
        self.create_alien(x=x, y=y, row=row, alien_no=self.aliens_created)
        x += self.settings.alien_spacing * alien_width
        self.aliens_created += 1
      x = alien_width
      y += self.settings.alien_spacing * alien_height
      row += 1

  def check_edges(self):
    for alien in self.alien_group.sprites():
      if alien.check_edges(): return True
    return False

  def check_bottom(self):
    for alien in self.alien_group.sprites():
      if alien.check_bottom(): return True
    return False
  
  def update(self):
    delta_y = 0
    if self.check_edges():
      delta_y = self.settings.fleet_drop
      self.v.x *= -1
      
    if self.check_bottom(): self.ship.hit()
    
    # ship lasers taking out aliens
    # collisions = pg.sprite.groupcollide(self.ship.lasers.lasergroup(), self.alien_group, True, True)
    collisions = pg.sprite.groupcollide(self.alien_group, self.ship.lasers.lasergroup(), True, True)
    if len(collisions) > 0: 
      for alien in collisions:
        self.sound.play_pop()
        index = alien.timer.current_index()
        points = Alien.points[index]
        self.stats.score += points

        if alien.isdying is False:
          alien.isdying = True
          alien.explosiontimer.switch_to(f'boom{str(points)}')
          alien.timer = alien.explosiontimer
          self.dying_aliens.add(alien)

          # while alien.isdying:
          #   if alien.timer.current_image() == 0:
          #     alien.isdying = False
          #   else:
          #     alien.draw()

      self.sb.prep_score()
      self.sb.check_high_score()

    # laser-laser collisions
    collisions = pg.sprite.groupcollide(self.ship.lasers.lasergroup(), self.lasers.lasergroup(), 
                                        True, True)
    
    for alien in self.dying_aliens.sprites():
      if alien.timer.current_image() == 0:
        alien.kill()
      else:
        alien.draw()

    for alien in self.alien_group.sprites():
      alien.update(self.v, delta_y)

    # must have aliens to fire at the ship
    if self.alien_group and self.fire_every_counter % self.settings.aliens_fireevery == 0:
      n = randint(0, len(self.alien_group) - 1)
      self.alien_group.sprites()[n].fire(lasers=self.lasers)
      self.sound.play_alien_laser()
    self.fire_every_counter += 1

    # update the positions of all of the aliens' lasers (the ship updates its own lasers)
    self.lasers.update()

    # no more aliens -- time to re-create the fleet
    if not self.alien_group:
      self.lasers.empty()
      self.create_fleet()
      self.settings.increase_speed()
      self.stats.level += 1
      self.sb.prep_level()

    # aliens hitting the ship
    if pg.sprite.spritecollideany(self.ship, self.alien_group):
      self.ship.hit()

    # alien lasers taking out the ship
    if pg.sprite.spritecollideany(self.ship, self.lasers.lasergroup()):
      self.ship.hit()


if __name__ == '__main__':
  print("\nERROR: aliens.py is the wrong file! Run play from alien_invasions.py\n")
