from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://ds:password@localhost:5432/ds', echo=True)

Base = declarative_base()