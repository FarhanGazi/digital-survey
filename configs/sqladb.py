from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from configs.config import Config
from sqlalchemy.orm import sessionmaker

class DB():
  engine = create_engine(Config.database_url(), echo=True)
  Base = declarative_base()
  Session = sessionmaker(bind=engine)
  session = Session()
