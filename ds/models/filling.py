import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from ds.helpers.base import Base
from ds.models.user import User
from ds.models.survey import Survey
from ds.models.question import Question


class Filling(Base):
    __tablename__ = 'fillings'

    id = Column(Integer, primary_key=True)
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

    def __repr__(self):
        return "<Survey(id='%s', status='%s')>" % (self.id, self.status)


User.fillings = relationship(
    Filling, order_by=Filling.id, back_populates="user")
Survey.fillings = relationship(
    Filling, order_by=Filling.id, back_populates="survey")
Question.fillings = relationship(
    Filling, order_by=Filling.id, back_populates="question")
