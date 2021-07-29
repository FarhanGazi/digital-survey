from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user

from ds.models.user import User
from configs.sqladb import DB

bp = Blueprint("auth", __name__, url_prefix="/auth")

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
            return redirect(url_for("survey.list"))
        else:
            return redirect(url_for("auth.signin"))
    else:
        return render_template("auth/signin.html")
