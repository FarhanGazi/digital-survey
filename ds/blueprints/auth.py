from flask import Blueprint, request, render_template, redirect, url_for, g
from flask_login import login_user, login_required, logout_user, current_user

from ds.models.user import User
from configs.sqladb import DB

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = DB('ds')
        user = db.session.query(User).filter(
            User.email == email, User.password == password).first()
        if user:
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for("survey.list"))
            elif user.role == 'panelist':
                return redirect(url_for("filling.list"))
        else:
            return redirect(url_for("auth.signin"))
    else:
        return render_template("auth/signin.html")


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        password = request.form["password"]

        db = DB('ds')
        new_user = User(name=name, surname=surname,
                        email=email, role='panelist', password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth.signin"))
    elif request.method == "GET":
        return render_template("auth/signup.html")


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    g.user = None
    return redirect(url_for("auth.signin"))


@bp.route('/index')
@login_required
def index():
    if current_user.role == 'admin':
        return redirect(url_for("survey.list"))
    elif current_user.role == 'panelist':
        return redirect(url_for("filling.list"))

    return redirect(url_for("auth.signin"))
