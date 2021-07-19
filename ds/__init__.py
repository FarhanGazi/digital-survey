from flask import Flask
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.sql.expression import true

from configs.config import Config
from configs.sqladb import DB

from ds.helpers.auth import login_manager, requires_roles
from ds.helpers.base import Base
from ds.models.user import User
from ds.models.survey import Survey
from ds.models.question import Question
from ds.models.filling import Filling
from ds.models.answer import Answer
from ds.models.response import Response


def create_app():
    # Create Flask App
    app = Flask(__name__, instance_relative_config=True)

    # Connect to database
    db = DB('ds')
    Base.metadata.create_all(db.engine, checkfirst=true)

    # Create login manager
    app.config['SECRET_KEY'] = Config.secret_key
    login_manager.init_app(app)

    # new_user = User(name='Gino', surname='Buonvino', email='gino@buonvino.com', password='123', role='admin')
    # db.session.add(new_user)
    # db.session.commit()
    # user = db.session.query(User).filter(User.id==1).first()

    # print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    # print(user)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        user = db.session.query(User).filter(User.id == 1).first()
        login_user(user)
        return 'LOGGATO!'

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return 'LOGOUT!'

    @app.route('/hello')
    def hello():
        if current_user.is_authenticated:
            print(current_user)
            return 'AUTHATO!'
        return 'Hello, World!'

    @app.route('/admin')
    @login_required
    @requires_roles('admin')
    def admin():
        return 'ADMIN!'

    return app
