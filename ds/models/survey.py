from sqlalchemy import Column, String, Integer, ForeignKey, event, DDL, false
from sqlalchemy.orm import relationship

from ds.helpers.base import Base
from ds.models.user import User

class Survey(Base):
    __tablename__ = 'surveys'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=false)
    description = Column(String)
    status = Column(String, nullable=false, default='draft')
    user_id = Column(Integer, ForeignKey(User.id), nullable=false)

    user = relationship(User, back_populates="surveys")

    def __repr__(self):
        return "<Survey(title='%s', status='%s')>" % (self.title, self.status)


User.surveys = relationship(Survey, order_by=Survey.id, back_populates="user")

# func = DDL(
#     "CREATE FUNCTION admin_user() "
#     "RETURNS TRIGGER AS $$ "
#     "BEGIN "
#     "IF NEW.user_id NOT IN (SELECT id FROM users WHERE role = 'admin') THEN"
#     "RETURN NULL; "
#     "RETURN NEW;"
#     "END; $$ LANGUAGE PLPGSQL"
# )

# trigger = DDL(
#     "CREATE TRIGGER dt_ins BEFORE INSERT ON surveys "
#     "FOR EACH ROW EXECUTE PROCEDURE admin_user();"
# )

# event.listen(
#     Survey.__tablename__,
#     'before_commit',
#     trigger.execute_if(dialect='postgresql')
# )
