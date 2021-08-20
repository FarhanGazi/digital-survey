<<<<<<< HEAD
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
=======
from flask import Blueprint, request, render_template, redirect, url_for, g
from flask_login import login_user, login_required, logout_user, current_user
>>>>>>> c98811db650ae2ddba4619e10e61d0fb3a16bdd4

from ds.models.user import User
from configs.sqladb import DB

bp = Blueprint("auth", __name__, url_prefix="/auth")


<<<<<<< HEAD
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
=======
@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
>>>>>>> c98811db650ae2ddba4619e10e61d0fb3a16bdd4
        email = request.form["email"]
        password = request.form["password"]
        db = DB('ds')
        user = db.session.query(User).filter(
            User.email == email, User.password == password).first()
        if user:
            login_user(user)
<<<<<<< HEAD
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("auth.signin"))
    else:
        return render_template("signin.html")
=======
            if user.role == 'admin':
                return redirect(url_for("survey.list"))
            elif user.role == 'panelist':
                return redirect(url_for("filling.list"))
        else:
            return redirect(url_for("auth.signin"))
    else:
        return render_template("auth/signin.html")
>>>>>>> c98811db650ae2ddba4619e10e61d0fb3a16bdd4


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
<<<<<<< HEAD
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
        return render_template("signup.html")

=======
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
>>>>>>> c98811db650ae2ddba4619e10e61d0fb3a16bdd4
