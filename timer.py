class Timer: 
  def __init__(self, image_list, start_index=0, delta=6, looponce=False): 
    self.image_list = image_list
    self.delta = delta
    self.looponce = looponce
    self.index = start_index
    self.time = 0

  def update_index(self):
    self.time += 1
    if self.time >= self.delta:
      self.index += 1
      self.time = 0
    
    if self.index >= len(self.image_list) and not self.looponce:
        self.index = 0

  def finished(self): 
    return self.looponce and self.index >= len(self.image_list)-1
  
  def current_index(self): return self.index

  def current_image(self):
    if not self.finished():
      self.update_index()
      return self.image_list[self.current_index()]
    else:
      return 0
  
class TimerDict(Timer):
  def __init__(self, dictionary, start_key, delta=6, looponce = False):
    super().__init__(dictionary[start_key], start_index = 0, delta = delta, looponce = looponce)
    self.dictionary = dictionary
    self.start_key = start_key
    self.current_key = self.start_key

  def has_key(self, name):
    for key in self.dictionary.keys():
      if key == name:
        return True
      
    return False

  def keys(self): return list(self.dictionary.keys())

  def switch_to(self, key):
    self.image_list = self.dictionary[key]
    self.current_key = key