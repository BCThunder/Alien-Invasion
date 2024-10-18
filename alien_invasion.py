import sys, time
import pygame as pg
from settings import Settings 
from ship import Ship
from aliens import Aliens
from vector import Vector
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from barriers import Barriers
from launch import Launch
from sound import Sound
from ufo import UFO

class Game:
  key_velocity = {pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1,  0)}
                  # pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1)}

  def __init__(self):
    pg.init()
    self.settings = Settings()
    self.screen = pg.display.set_mode(
      (self.settings.screen_width, self.settings.screen_height))
    pg.display.set_caption("Alien Invasion")

    self.aliens = None
    self.sound = Sound()
    self.stats = GameStats(game=self)
    self.sb = Scoreboard(game=self)
    # self.launch = Launch(game=self)

    self.ship = Ship(game=self)
    self.aliens = Aliens(game=self)
    self.barriers = Barriers(game=self)
    self.ufo = UFO(game=self)
    self.ship.set_aliens(self.aliens)
    self.ship.set_sb(self.sb)
    self.game_active = False              # MUST be before Button is created
    self.first = True
    self.play_button = Button(game=self, text='Play')

  def check_events(self):
    for event in pg.event.get():
      type = event.type
      if type == pg.KEYUP: 
        key = event.key 
        if key == pg.K_SPACE: self.ship.cease_fire()
        elif key in Game.key_velocity: self.ship.all_stop()
      elif type == pg.QUIT: 
        pg.quit()
        sys.exit()
      elif type == pg.KEYDOWN:
        key = event.key
        if key == pg.K_SPACE: 
          self.ship.fire_everything()
        elif key == pg.K_p: 
          self.play_button.select(True)
          self.play_button.press()
        elif key in Game.key_velocity: 
          self.ship.add_speed(Game.key_velocity[key])
      elif type == pg.MOUSEBUTTONDOWN:
        b = self.play_button
        x, y = pg.mouse.get_pos()
        if b.rect.collidepoint(x, y):
          b.press()
      elif type == pg.MOUSEMOTION:
        b = self.play_button
        x, y = pg.mouse.get_pos()
        b.select(b.rect.collidepoint(x, y))
    
  def restart(self):
    self.screen.fill(self.settings.bg_color)
    self.ship.reset()
    self.aliens.reset()
    self.barriers.reset()
    self.ufo.reset()
    self.settings.initialize_dynamic_settings()

  def game_over(self):
    print('Game Over !')
    pg.mouse.set_visible(True)
    self.play_button.change_text('Play again?')
    self.play_button.show()
    self.first = True
    self.game_active = False

    hs_file = open("highscore.json", "w")
    hs_file.write(str(self.sb.high_score))
    hs_file.close()

    self.stats.reset()
    self.restart()
    self.sound.play_game_over()

  def activate(self): 
    self.game_active = True
    self.first = False
    self.sound.play_music("sounds/our_hearts_collide.wav")

  def play(self):
    launch = Launch(game=self)
    launch.start()

    finished = False
    self.screen.fill(self.settings.bg_color)

    while not finished:
      self.check_events()    # exits if Cmd-Q on macOS or Ctrl-Q on other OS

      if self.game_active or self.first:
        self.first = False
        self.screen.fill(self.settings.bg_color)
        self.ship.update()
        self.aliens.update()
        self.barriers.update()
        self.sb.update()
        self.ufo.update()
      else:
        self.play_button.update()
      
      pg.display.flip()
      time.sleep(0.02)


if __name__ == '__main__':
  g = Game()
  g.play()

