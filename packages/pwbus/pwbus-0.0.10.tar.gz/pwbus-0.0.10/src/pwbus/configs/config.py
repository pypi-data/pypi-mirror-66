### PWBus - Config Class 
#:  Load file: etc/pwbus.json
#:
#:  maintainer: fabio.szostak@perfweb.com.br | Sat Nov 16 16:36:36 -03 2019

from json import load

class Config():

  def __init__(self):
    with open('etc/engine.json') as json_file:
      self.config_data = load(json_file)

  ## Config.get
  #
  def get(self, name):
    if name in self.config_data:
      return self.config_data[name]
    return None
  