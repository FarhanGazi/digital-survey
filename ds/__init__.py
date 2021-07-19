from flask import Flask
from flask_login import current_user, login_user, logout_user, login_required

from configs.config import Config
from configs.sqladb import DB
from ds.helpers.auth import login_manager, requires_roles
from ds.models.user import *

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = Config.secret_key

    DB.Base.metadata.create_all(DB.engine)
    login_manager.init_app(app)

    # new_user = User(name='Gino', surname='Buonvino', email='gino@buonvino.com', password='123', role='Admin')
    # session.add(new_user)
    # session.commit()
    # user = session.query(User).filter(User.id==1).first()

    # print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    # print(user)

    # @app.route('/login', methods=['GET', 'POST'])
    # def login():
    #     user = session.query(User).filter(User.id == 1).first()
    #     login_user(user)
    #     return 'LOGGATO!'

    # @app.route('/logout')
    # @login_required
    # def logout():
    #     logout_user()
    #     return 'LOGOUT!'

    # @app.route('/hello')
    # def hello():
    #     if current_user.is_authenticated:
    #         print(current_user)
    #         return 'AUTHATO!'
    #     return 'Hello, World!'

    # @app.route('/admin')
    # @login_required
    # @requires_roles('admin')
    # def admin():
    #     return 'ADMIN!'

    return app
