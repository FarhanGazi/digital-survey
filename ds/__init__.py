from flask import Flask
from configs.config import *
from configs.sqladb import *
from ds.models.user import *

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    Base.metadata.create_all(engine)

    print (databasename)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app