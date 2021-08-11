import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import event
from sqlalchemy.orm.exc import FlushError

from configs.sqladb import DB
from ds.helpers.base import Base
from ds.models.user import User


class Survey(Base):
    __tablename__ = 'surveys'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, CheckConstraint(
        "status IN ('draft', 'active', 'inactive')"), nullable=False, default='draft')
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    created_at = Column('created_at', DateTime, default=datetime.datetime.now)
    updated_at = Column('updated_at', DateTime,
                        default=datetime.datetime.now, onupdate=datetime.datetime.now)

    user = relationship(User, back_populates='surveys')
    responses = relationship(
        "Response", back_populates="survey", cascade="all, delete, delete-orphan")
    questions = relationship("Question", order_by="Question.seq",
                             back_populates="survey", cascade="all, delete, delete-orphan")
    fillings = relationship(
        "Filling", back_populates="survey", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<Survey(title='%s', status='%s')>" % (self.title, self.status)


##########################################
# SQL-ALCHEMY TRIGGERS ALTERNATIVE
##########################################

@event.listens_for(Survey, 'before_insert')
@event.listens_for(Survey, 'before_update')
def check_users_role(mapper, connection, target):
    db = DB('ds')
    user = db.session.query(User).filter(User.id == target.user_id).first()
    if user.role not in ['admin']:
        raise FlushError
