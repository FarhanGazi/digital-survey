from flask import Flask

from configs.sqladb import Base, engine
from ds.models.user import *

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    Base.metadata.create_all(engine)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app