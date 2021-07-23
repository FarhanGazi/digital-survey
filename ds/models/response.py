import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from ds.helpers.base import Base
from ds.models.user import User
from ds.models.question import Question
from ds.models.answer import Answer


class Response(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    response = Column(String)
    type = Column(String, CheckConstraint(
        "type IN ('radio', 'multiple', 'text')"), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    question_id = Column(Integer, ForeignKey(Question.id), nullable=False)
    answer_id = Column(Integer, ForeignKey(Answer.id))

    created_at = Column('created_at', DateTime, default=datetime.datetime.now)
    updated_at = Column('updated_at', DateTime,
                        default=datetime.datetime.now, onupdate=datetime.datetime.now)

    user = relationship(User, back_populates="responses")
    question = relationship(Question, back_populates="responses")
    answer = relationship(Answer, back_populates="responses")

    def __repr__(self):
        return "<Survey(response='%s', type='%s')>" % (self.response, self.type)


User.responses = relationship(
    Response, order_by=Response.id, back_populates="user")
Question.responses = relationship(
    Response, order_by=Response.id, back_populates="question")
Answer.responses = relationship(
    Response, order_by=Response.id, back_populates="answer")
