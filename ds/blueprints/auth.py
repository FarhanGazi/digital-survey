from flask import Blueprint, render_template, request
from flask_login import login_user

from ds.models.user import User
from configs.sqladb import DB

bp = Blueprint("auth", __name__, url_prefix="/auth")



# @bp.route('/login', methods=['GET', 'POST'])
# def login():
#     db = DB('ds')
#     user = db.session.query(User).filter(User.id == 1).first()
#     login_user(user)
#     return render_template("homepage.html")



@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    email = request.form["emailAddress"]
    if request.method == "POST" and email == "aaaa" :
        # email = request.form["emailAddress"]
        # password = request.form["password"]
        # db = DB('ds')
        # user = db.session.query(User).filter(User.email == email, User.password == password).first()
        # login_user(user)
        return render_template("homepage.html")
    else:
        return render_template("signin.html")    

