import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy import event
from sqlalchemy.orm.exc import FlushError

from ds.helpers.base import Base
from configs.sqladb import DB
from ds.models.user import User
from ds.models.survey import Survey
from ds.models.question import Question


class Filling(Base):
    __tablename__ = 'fillings'

    id = Column(Integer, primary_key=True)
    is_last = Column(Boolean, default=False)
    status = Column(String, CheckConstraint(
        "status IN ('completed', 'incomplete')"), nullable=False, default='incomplete')

    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    survey_id = Column(Integer, ForeignKey(Survey.id), nullable=False)
    question_id = Column(Integer, ForeignKey(Question.id), nullable=False)

    created_at = Column('created_at', DateTime, default=datetime.datetime.now)
    updated_at = Column('updated_at', DateTime,
                        default=datetime.datetime.now, onupdate=datetime.datetime.now)

    user = relationship(User, back_populates="fillings")
    survey = relationship(Survey, back_populates="fillings")
    question = relationship(Question, back_populates="fillings")

    responses = relationship(
        "Response", back_populates="filling", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<Filling(id='%s', status='%s')>" % (self.id, self.status)

##########################################
# SQL-ALCHEMY INDEX ALTERNATIVE
##########################################


Index('user_survey_filling', Filling.user_id,
      Filling.survey_id, unique=True)

##########################################
# SQL-ALCHEMY TRIGGERS ALTERNATIVE
##########################################


@event.listens_for(Filling, 'before_insert')
@event.listens_for(Filling, 'before_update')
def check_users_role(mapper, connection, target):
    db = DB('ds')
    user = db.session.query(User).filter(User.id == target.user_id).first()
    if user.role not in ['panelist']:
        raise FlushError
