from flask import Blueprint
from flask_login import login_user

from ds.models.user import User
from configs.sqladb import DB

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route('/login', methods=['GET', 'POST'])
def login():
    db = DB('ds')
    user = db.session.query(User).filter(User.id == 1).first()
    login_user(user)
    return 'LOGGATO!'
