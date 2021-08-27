from flask import Blueprint, request, render_template, redirect, url_for
from flask.helpers import flash
from flask_login import current_user, login_required

from ds.models.user import User
from configs.sqladb import DB

bp = Blueprint("profile", __name__, url_prefix="/profile")


######################################################################################
# PROFILE UPDATE
#
# Endpoint: /profile/update
# Parameteres: -
# When in GET shows user profile update with its data, when in POST saves new data
######################################################################################
@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        try:
            name = request.form["name"]
            surname = request.form["surname"]
            email = request.form["email"]
            password = request.form["password"]

            db = DB('ds')
            user = db.session.query(User).filter(
                User.id == current_user.id).first()
            user.name = name
            user.surname = surname
            user.email = email
            user.password = password
            db.session.commit()

            return redirect(url_for("auth.index"))
        except:
            db.session.rollback()
            flash('Alcuni campi non sono validi!')
            return redirect(url_for("profile.update"))

    elif request.method == 'GET':
        db = DB('ds')
        user = db.session.query(User).filter(
            User.id == current_user.id).first()
        return render_template("profile/update.html", user=user)
