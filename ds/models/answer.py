from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.traversals import ANON_NAME

from ds.helpers.base import Base
from ds.models.question import Question


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    answer = Column(String, nullable=False)
    status = Column(String, nullable=False, default='active')
    question_id = Column(Integer, ForeignKey(Question.id), nullable=False)

    question = relationship(Question, back_populates="answers")

    def __repr__(self):
        return "<Survey(answer='%s', status='%s')>" % (self.answer, self.status)

Question.answers = relationship(Answer, order_by=Answer.id, back_populates="question")
