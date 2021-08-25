import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from ds.helpers.base import Base
from ds.models.survey import Survey


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, CheckConstraint(
        "status IN ('draft', 'active', 'inactive')"), nullable=False, default='draft')
    type = Column(String, CheckConstraint(
        "type IN ('radio', 'multiple', 'text')"), nullable=False)
    survey_id = Column(Integer, ForeignKey(Survey.id), nullable=False)
    seq = Column(Integer, nullable=False, default=1)

    created_at = Column('created_at', DateTime, default=datetime.datetime.now)
    updated_at = Column('updated_at', DateTime,
                        default=datetime.datetime.now, onupdate=datetime.datetime.now)

    survey = relationship(Survey, back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete, delete-orphan")
    responses = relationship("Response", back_populates="question", cascade="all, delete, delete-orphan")
    fillings = relationship("Filling", back_populates="question", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<Question(title='%s', status='%s')>" % (self.title, self.status)
