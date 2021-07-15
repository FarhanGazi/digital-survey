import confuse
from os import path

config = confuse.Configuration('Digital-Survey', __name__)

if path.isfile('config.yaml'):
  config.set_file('config.yaml', base_for_paths=True)
else:
  config.set_file('default_config.yaml')


class Config():
  database = config['database']

  driver = database['driver'].get()
  username = database['username'].get()
  password = database['password'].get()
  host = database['host'].get()
  port = database['port'].get()
  databasename = database['databasename'].get()

  @staticmethod
  def database_url():
    return f'{Config.driver}://{Config.username}:{Config.password}@{Config.host}:{Config.port}/{Config.databasename}'