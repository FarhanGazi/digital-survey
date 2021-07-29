from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_required

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
