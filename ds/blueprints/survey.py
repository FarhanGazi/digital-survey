from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql.functions import user

from ds.helpers.auth import requires_roles
from ds.models.user import User
from ds.models.survey import Survey
from configs.sqladb import DB

bp = Blueprint("survey", __name__, url_prefix="/surveys")

@bp.route('/', methods=['GET'])
@login_required
@requires_roles('admin')
def list():
  return render_template("admin/surveys/list.html")


@bp.route('/<int:id>', methods=['GET'])
@login_required
@requires_roles('admin')
def details(id):
    db = DB('ds')
    survey = db.session.query(Survey).filter(Survey.id == id, Survey.user_id == current_user.id).first()
    return render_template("admin/surveys/details.html", survey=survey)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def create():
  if request.method == 'POST':
    title = request.form["title"]
    description = request.form["description"]

    db = DB('ds')
    new_surevy = Survey(title=title, description=description, user_id=current_user.id)
    db.session.add(new_surevy)
    db.session.commit()

    return redirect(url_for("survey.details", id=new_surevy.id))

  elif request.method == 'GET':
    return render_template("admin/surveys/create.html")
