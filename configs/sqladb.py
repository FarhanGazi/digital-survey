from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from configs.config import Config

engine = create_engine(Config.database_url(), echo=True)

Base = declarative_base()