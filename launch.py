import pygame as pg
import sys, time
from button import Button
from aliens import Alien
from ufo import UFO_SPRITE

class Launch:
    def __init__(self, game):
        self.game = game
        self.aliens = Alien(game = self.game, row = 0, alien_no = 0)
        self.ufo = UFO_SPRITE(game = self.game)
        self.ufo_image = self.ufo.get_ufo_data()
        self.alien_images, self.alien_points = self.aliens.get_alien_data()
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.finished = False
        
        self.play_button = Button(self.game, text = 'Play')
        self.b_rect = self.play_button.rect
        self.buttons_y = self.screen_rect.centery + 200
        self.play_button.change_button_center((self.b_rect.centerx, self.buttons_y))

        self.hs_button = Button(self.game, text = 'High Score')
        self.hs_b_rect = self.hs_button.rect
        self.hs_button.change_button_center((self.hs_b_rect.centerx, self.buttons_y + self.b_rect.height + 20))
        self.show_hs = False

        self.back_button = Button(self.game, text = "Go Back")
        self.back_b_rect = self.back_button.rect
        self.back_button.change_button_center((self.back_b_rect.centerx, self.screen_rect.centery + 200))

    def draw(self):
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen.fill((0, 0, 0))
        font = pg.font.SysFont("Impact", 100)
        point_font = pg.font.SysFont("Impact", 25)
        text = font.render("Space Invaders", True, (255, 255, 255))

        x, y = (285, 230)
        index = 0
        for image in self.alien_images:
            point_text = point_font.render(str(self.alien_points[index]), True, (255, 255, 255))
            self.screen.blit(image, (x - image.get_width()/2, y))
            self.screen.blit(point_text, (x - point_text.get_width()/2, y + image.get_height() + 10))

            x += 125
            index += 1

        ufo_point_text = point_font.render("???", True, (255, 255, 255))
        ufo_x, ufo_y = self.settings.screen_width/2 - self.ufo_image.get_width()/2, self.screen_rect.centery + 20
        self.screen.blit(self.ufo_image, (ufo_x, ufo_y))
        self.screen.blit(ufo_point_text, (self.settings.screen_width/2 - ufo_point_text.get_width()/2, ufo_y + self.ufo_image.get_rect().height + 10))

        self.screen.blit(text, (self.settings.screen_width/2 - text.get_width()/2, 20))
        self.play_button.update()
        self.hs_button.update()
        pg.display.update()

    def check_events(self):
        for event in pg.event.get():
            type = event.type
            if type == pg.QUIT: 
                pg.quit()
                sys.exit()
            elif type == pg.KEYDOWN:
                key = event.key
                if key == pg.K_p: 
                    self.play_button.select(True)
                    self.play_button.press('game')
            elif type == pg.MOUSEBUTTONDOWN:
                play_b = self.play_button
                hs_b = self.hs_button
                x, y = pg.mouse.get_pos()

                if play_b.rect.collidepoint(x, y):
                    play_b.press('game')
                    self.finished = True
                elif hs_b.rect.collidepoint(x, y):
                    self.show_hs = hs_b.press('hs')

            elif type == pg.MOUSEMOTION:
                play_b = self.play_button
                hs_b = self.hs_button
                x, y = pg.mouse.get_pos()
                play_b.select(play_b.rect.collidepoint(x, y))
                hs_b.select(hs_b.rect.collidepoint(x, y))

    def draw_hs_screen(self):
        self.screen.fill((0, 0, 0))
        hs_file = open("highscore.json", "r")
        high_score = hs_file.read()
        hs_file.close()

        hs_text = f"High Score: {high_score}"
        font = pg.font.SysFont("Impact", 100)
        text = font.render(hs_text, True, (255, 255, 255))
        self.screen.blit(text, (self.settings.screen_width/2 - text.get_width()/2, 100))
        self.back_button.update()
        pg.display.update()

    def check_hs_events(self):
        for event in pg.event.get():
            type = event.type
            if type == pg.QUIT: 
                pg.quit()
                sys.exit()
            elif type == pg.MOUSEBUTTONDOWN:
                back_b = self.back_button
                x, y = pg.mouse.get_pos()

                if back_b.rect.collidepoint(x, y):
                    self.show_hs = False
                    self.draw()
                    self.hs_button.show()

            elif type == pg.MOUSEMOTION:
                back_b = self.back_button
                x, y = pg.mouse.get_pos()
                back_b.select(back_b.rect.collidepoint(x, y))

    def start(self):
        self.draw()

        while not self.finished:
            self.check_events()
            self.play_button.update()
            self.hs_button.update()

            if self.show_hs:
                self.draw_hs_screen()
                while self.show_hs:
                    self.back_button.update()
                    self.check_hs_events()

                    pg.display.flip()
                    time.sleep(0.02)

            pg.display.flip()
            time.sleep(0.02)