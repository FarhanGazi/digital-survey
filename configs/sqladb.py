from sqlalchemy import create_engine
from configs.config import Config
from sqlalchemy.orm import sessionmaker

class DB:
    class __DB:
        def __init__(self, arg):
            self.username = arg

            if self.username in ['ds', 'admin', 'panelist']:
              config = Config(self.username)
              self.engine = create_engine(config.database_url, echo=True)
              self.Session = sessionmaker(
                  bind=self.engine, expire_on_commit=False)
              self.session = self.Session()

        def __str__(self):
            return repr(self) + self.username

    instance = None

    def __init__(self, arg):
        if not DB.instance:
            DB.instance = DB.__DB(arg)
        else:
          if DB.instance.username != arg:
            DB.instance = DB.__DB(arg)

    def __getattr__(self, name):
        return getattr(self.instance, name)
