import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy import event
from sqlalchemy.orm.exc import FlushError

from configs.sqladb import DB
from ds.helpers.base import Base
from ds.models.user import User
from ds.models.survey import Survey
from ds.models.filling import Filling
from ds.models.question import Question
from ds.models.answer import Answer


class Response(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    type = Column(String, CheckConstraint(
        "type IN ('radio', 'multiple', 'text')"), nullable=False)
    response = Column(String, CheckConstraint(
        "(type <> 'text') OR (response IS NOT NULL)"))
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    filling_id = Column(Integer, ForeignKey(Filling.id), nullable=False)
    survey_id = Column(Integer, ForeignKey(Survey.id), nullable=False)
    question_id = Column(Integer, ForeignKey(Question.id), nullable=False)
    answer_id = Column(Integer, ForeignKey(Answer.id))

    created_at = Column('created_at', DateTime, default=datetime.datetime.now)
    updated_at = Column('updated_at', DateTime,
                        default=datetime.datetime.now, onupdate=datetime.datetime.now)

    user = relationship(User, back_populates="responses")
    filling = relationship(Filling, back_populates="responses")
    survey = relationship(Survey, back_populates="responses")
    question = relationship(Question, back_populates="responses")
    answer = relationship(Answer, back_populates="responses")

    def __repr__(self):
        return "<Response(response='%s', type='%s')>" % (self.response, self.type)


##########################################
<<<<<<< HEAD
# SQL-ALCHEMY TRIGGERS ALTERNATIE
=======
# SQL-ALCHEMY INDEX ALTERNATIVE
##########################################

Index('user_response', Response.user_id,
      Response.question_id, unique=True)

##########################################
# SQL-ALCHEMY TRIGGERS ALTERNATIVE
>>>>>>> 87e8b18723781b961b90a05778a30f446ebee4c3
##########################################

@event.listens_for(Response, 'before_insert')
@event.listens_for(Response, 'before_update')
def check_radio(mapper, connection, target):
    db = DB('ds')
    if target.type == 'radio':
        response = db.session.query(Response).filter(Response.user_id == target.user_id, Response.survey_id ==
                                                     target.survey_id, Response.question_id == target.question_id, Response.answer_id == target.answer_id).first()
        if response:
            raise FlushError
