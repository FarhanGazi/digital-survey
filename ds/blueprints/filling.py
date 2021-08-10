from ds.models.question import Question
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql.expression import select

from ds.helpers.auth import requires_roles
from ds.models.answer import Answer
from ds.models.filling import Filling
from ds.models.response import Response
from ds.models.survey import Survey
from configs.sqladb import DB

bp = Blueprint("filling", __name__, url_prefix="/fillings")


@bp.route('/', methods=['GET'])
@login_required
@requires_roles('panelist')
def list():
    db = DB('ds')
    surveys = db.session.query(Survey).filter(Survey.id.not_in(select(Filling.survey_id).where(
        Filling.status == 'completed', Filling.user_id == current_user.id).subquery()), Survey.status == 'active').order_by(Survey.id.asc()).all()

    return render_template("fillings/list.html", surveys=surveys)


@bp.route('/start/<int:survey_id>', methods=['GET'])
@login_required
@requires_roles('panelist')
def start(survey_id):
    db = DB('ds')
    survey = db.session.query(Survey).filter(Survey.id == survey_id).first()
    filling = db.session.query(Filling).filter(
        Filling.survey_id == survey.id, Filling.user_id == current_user.id).first()
    if filling is None:
        filling = Filling(status='incomplete', user_id=current_user.id,
                          survey_id=survey.id, question_id=survey.questions[0].id)
        db.session.add(filling)
        db.session.commit()

    return redirect(url_for("filling.get", filling_id=filling.id))


@bp.route('/<int:filling_id>', methods=['GET'])
@login_required
@requires_roles('panelist')
def get(filling_id):
    db = DB('ds')
    filling = db.session.query(Filling).filter(
        Filling.id == filling_id, Filling.user_id == current_user.id).first()
    question = db.session.query(Question).filter(
        Question.id == filling.question_id, Question.survey_id == filling.survey_id, Question.status == 'active').first()
    question.filling_id = filling_id

    return render_template("fillings/question.html", question=question)


@bp.route('/<int:filling_id>/save', methods=['GET', 'POST'])
@login_required
@requires_roles('panelist')
def save(filling_id):
    if request.method == 'POST':
      type = request.form['type']
      db = DB('ds')
      filling = db.session.query(Filling).filter(Filling.id == filling_id, Filling.user_id == current_user.id).first()

      if type == 'radio':
        answer_id = request.form['answer']
        response = Response(type=filling.question.type, user_id=current_user.id, question_id=filling.question_id, answer_id=answer_id)
        db.session.add(response)
        db.session.commit()



    return
