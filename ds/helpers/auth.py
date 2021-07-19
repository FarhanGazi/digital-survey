from functools import wraps
from flask_login import LoginManager, current_user

from configs.sqladb import DB
from ds.models.user import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    db = DB('ds')
    user = db.session.query(User).filter(User.id == user_id).first()
    return user


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                return "You are not authorized to access this page"
            return f(*args, **kwargs)
        return wrapped
    return wrapper
