import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from ds.helpers.base import Base
from ds.models.question import Question


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    answer = Column(String, nullable=False)
    status = Column(String, CheckConstraint(
        "status IN ('draft', 'active', 'inactive')"), nullable=False, default='draft')
    question_id = Column(Integer, ForeignKey(Question.id), nullable=False)

    created_at = Column('created_at', DateTime, default=datetime.datetime.now)
    updated_at = Column('updated_at', DateTime,
                        default=datetime.datetime.now, onupdate=datetime.datetime.now)

    question = relationship(Question, back_populates="answers")
    responses = relationship(
        "Response", back_populates="answer", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<Survey(answer='%s', status='%s')>" % (self.answer, self.status)
