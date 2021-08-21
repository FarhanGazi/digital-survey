from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_required

from ds.models.user import User
from configs.sqladb import DB

bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        password = request.form["password"]

        db = DB('ds')
        user = db.session.query(User).filter(User.id == current_user.id).first()
        user.name = name
        user.surname = surname
        user.email = email
        user.password = password
        db.session.commit()

        return redirect(url_for("auth.index"))

    elif request.method == 'GET':
        db = DB('ds')
        user = db.session.query(User).filter(User.id == current_user.id).first()
        return render_template("profile/update.html", user=user)
