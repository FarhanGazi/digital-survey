from flask import Blueprint, request, render_template, redirect, url_for, g
from flask.helpers import flash
from flask_login import login_user, login_required, logout_user, current_user

from ds.models.user import User
from configs.sqladb import DB

bp = Blueprint("auth", __name__, url_prefix="/auth")


######################################################################################
# AUTH SIGNIN
#
# Endpoint: /auth/signin
# Parameteres: -
# When in GET shows signin FORM, when in POST executes signin and redirects home
######################################################################################
@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]
            db = DB('ds')
            user = db.session.query(User).filter(
                User.email == email, User.password == password).first()
        except:
            db.session.rollback()
            flash('Qualcosa è andato storto!')
            return redirect(url_for("auth.signin"))

        if user:
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for("survey.list"))
            elif user.role == 'panelist':
                return redirect(url_for("filling.list"))
        else:
            flash('Credenziali non valide!')
            return redirect(url_for("auth.signin"))
    else:
        return render_template("auth/signin.html")


######################################################################################
# AUTH SIGNUP
#
# Endpoint: /auth/signup
# Parameteres: -
# When in GET shows signup FORM, when in POST registres new user
######################################################################################
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        try:
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
        except:
            db.session.rollback()
            flash('Utente già esistente!')
            return redirect(url_for("auth.signup"))

    elif request.method == "GET":
        return render_template("auth/signup.html")


######################################################################################
# AUTH LOGOUT
#
# Endpoint: /auth/logout
# Parameteres: -
# Logouts the user
######################################################################################
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    g.user = None
    return redirect(url_for("auth.signin"))


######################################################################################
# AUTH INDEX
#
# Endpoint: /auth/index
# Parameteres: -
# Redirects to the right home path based on user role
######################################################################################
@bp.route('/index')
@login_required
def index():
    if current_user.role == 'admin':
        return redirect(url_for("survey.list"))
    elif current_user.role == 'panelist':
        return redirect(url_for("filling.list"))

    return redirect(url_for("auth.signin"))
