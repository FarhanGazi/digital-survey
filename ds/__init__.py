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

import ds.blueprints.auth as authentication


def create_app():
    # Create Flask App
    app = Flask(__name__, instance_relative_config=True)

    # Connect to database
    db = DB('ds')
    Base.metadata.create_all(db.engine, checkfirst=true)

    # Create login manager
    config = Config('ds')
    app.config['SECRET_KEY'] = config.secret_key
    login_manager.init_app(app)

    app.register_blueprint(authentication.bp)

    # new_user = User(name='Gino', surname='Buonvino', email='gino@buonvino.com', password='123', role='admin')
    # db.session.add(new_user)
    # db.session.commit()
    # user = db.session.query(User).filter(User.id==1).first()

    # print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    # print(user)

    @app.route('/create', methods=['GET', 'POST'])
    def create():
        new_user = User(name='Gino', surname='Buonvino',
                        email='gino@buonvino.com', password='123', role='admin')
        db.session.add(new_user)
        db.session.commit()
        new_survey = Survey(title='Survey1', description='Desc...', status='active', user_id=new_user.id)
        db.session.add(new_survey)
        db.session.commit()
        return 'FATTO!'

    @app.route('/delete', methods=['GET', 'POST'])
    def delete():
        user = db.session.query(User).filter(User.id == 2).first()
        surveys = user.surveys
        print(surveys)
        #survey = db.session.query(Survey).filter(Survey.user_id == user.id).first
        db.session.delete(user)
        db.session.commit()
        return surveys[0].title

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
