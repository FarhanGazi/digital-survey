from os import name
from flask import Flask

from configs.sqladb import Base, engine, session
from ds.models.user import *

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    Base.metadata.create_all(engine)

    # new_user = User(name='Gino', surname='Buonvino', email='ginobuonvino.com', password='123', role='Admin')
    # session.add(new_user)
    # session.commit()

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app