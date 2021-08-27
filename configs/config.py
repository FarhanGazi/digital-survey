import confuse
from os import path


######################################################################################
# CONFIGURATION CLASS - SINGLETON PATTERN
# Loades configurations based on roles
######################################################################################
class Config:
    class __Config:
        def __init__(self, arg):
            config = confuse.Configuration('Digital-Survey', __name__)
            if path.isfile('config.yaml'):
                config.set_file('config.yaml', base_for_paths=True)
            else:
                config.set_file('default_config.yaml')

            self.username = arg
            if self.username in ['ds', 'admin', 'panelist']:
                config = config[self.username]
                database = config['database']
                application = config['application']

                self.driver = database['driver'].get()
                self.username = database['username'].get()
                self.password = database['password'].get()
                self.host = database['host'].get()
                self.port = database['port'].get()
                self.databasename = database['databasename'].get()
                self.secret_key = application['secretkey'].get()
                self.database_url = f'{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.databasename}'

        def __str__(self):
            return repr(self) + self.username

    instance = None

    def __init__(self, arg):
        if not Config.instance:
            Config.instance = Config.__Config(arg)
        else:
            if Config.instance.username != arg:
                Config.instance = Config.__Config(arg)

    def __getattr__(self, name):
        return getattr(self.instance, name)
