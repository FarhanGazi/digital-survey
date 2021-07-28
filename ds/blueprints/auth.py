from flask import Blueprint, render_template, request, redirect, url_for, flash
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
    if request.method == "POST":
        print(request.form)
        email = request.form["email"]
        password = request.form["password"]
        db = DB('ds')
        user = db.session.query(User).filter(
            User.email == email, User.password == password).first()
        if user:
            login_user(user)
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("auth.signin"))
    else:
        return render_template("signin.html")
