from configs.sqladb import *
from sqlalchemy.orm import validates

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, nullable=false)
    password = Column(String, nullable=false)
    role = Column(String, nullable=false)

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    def __repr__(self):
        return "<User(enail='%s', role='%s')>" % (self.enail, self.role)