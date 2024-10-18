class GameStats:
  def __init__(self, game):
    self.game = game 
    self.settings = game.settings
    self.ships_left = 0
    self.reset()
    hs_file = open("highscore.json", "r")
    self.high_score = int(hs_file.read())
    hs_file.close()

  def reset(self):
    self.ships_left = self.settings.ship_limit
    self.score = 0
    self.level = 1
