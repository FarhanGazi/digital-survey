from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from ds.helpers.base import Base
from ds.models.survey import Survey


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, nullable=False, default='draft')
    type = Column(String, CheckConstraint("type IN ('radio', 'multiple', 'text')"), nullable=False)
    seq = Column(Integer, nullable=False)
    survey_id = Column(Integer, ForeignKey(Survey.id), nullable=False)

    survey = relationship(Survey, back_populates="questions")

    def __repr__(self):
        return "<Survey(title='%s', status='%s')>" % (self.title, self.status)


Survey.questions = relationship(Question, order_by=Question.seq, back_populates="survey")
