from flask import Flask

from configs.config import Config
from configs.sqladb import DB

from ds.helpers.auth import login_manager
from ds.helpers.base import Base

import ds.models.user
import ds.models.survey
import ds.models.question
import ds.models.filling
import ds.models.answer
import ds.models.response

import ds.blueprints.auth as authentication
import ds.blueprints.survey as survey
import ds.blueprints.question as question
import ds.blueprints.answer as answer
import ds.blueprints.user as user
import ds.blueprints.profile as profile
import ds.blueprints.filling as filling


def create_app():
    # Create Flask App
    app = Flask(__name__, instance_relative_config=True)

    # Connect to database
    db = DB('ds')
    Base.metadata.create_all(db.engine, checkfirst=True)

    # Create login manager
    config = Config('ds')
    app.config['SECRET_KEY'] = config.secret_key
    login_manager.init_app(app)

    # Register all blueprints
    app.register_blueprint(authentication.bp)
    app.register_blueprint(survey.bp)
    app.register_blueprint(question.bp)
    app.register_blueprint(answer.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(filling.bp)

    app.add_url_rule("/", endpoint="auth.index")

    return app
