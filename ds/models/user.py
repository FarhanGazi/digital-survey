import datetime

from sqlalchemy import Column, String, Integer, DateTime, CheckConstraint
from sqlalchemy.orm import validates
from flask_login import UserMixin

from ds.helpers.base import Base


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, CheckConstraint(
        "role IN ('admin', 'panelist')"), nullable=False)

    created_at = Column('created_at', DateTime, default=datetime.datetime.now)
    updated_at = Column('updated_at', DateTime,
                        default=datetime.datetime.now, onupdate=datetime.datetime.now)

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    def __repr__(self):
        return "<User(enail='%s', role='%s')>" % (self.email, self.role)
