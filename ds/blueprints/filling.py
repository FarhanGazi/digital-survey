from ds.models.question import Question
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy.sql.expression import select

from ds.helpers.auth import requires_roles
from ds.models.filling import Filling
from ds.models.response import Response
from ds.models.survey import Survey
from configs.sqladb import DB

bp = Blueprint("filling", __name__, url_prefix="/fillings")


@bp.route('/', methods=['GET'])
@login_required
@requires_roles('panelist')
def list():
    try:
        db = DB('panelist')
        surveys = db.session.query(Survey).filter(Survey.id.not_in(select(Filling.survey_id).where(
            Filling.status == 'completed', Filling.user_id == current_user.id).subquery()), Survey.status == 'active').order_by(Survey.id.asc()).all()
    except:
        flash('Qualcosa è andato storto!')

    return render_template("fillings/list.html", surveys=surveys)


@bp.route('/start/<int:survey_id>', methods=['GET'])
@login_required
@requires_roles('panelist')
def start(survey_id):
    try:
        db = DB('panelist')
        survey = db.session.query(Survey).filter(
            Survey.id == survey_id).first()
        filling = db.session.query(Filling).filter(
            Filling.survey_id == survey.id, Filling.user_id == current_user.id).first()
        if filling is None:
            filling = Filling(status='incomplete', user_id=current_user.id,
                              survey_id=survey.id, question_id=survey.questions[0].id, is_last=len(survey.questions) == 1)
            db.session.add(filling)
            db.session.commit()
    except:
        db.session.rollback()
        flash('Sondaggio non trovato!')

    return redirect(url_for("filling.get", filling_id=filling.id))


@bp.route('/<int:filling_id>', methods=['GET'])
@login_required
@requires_roles('panelist')
def get(filling_id):
    try:
        db = DB('panelist')
        filling = db.session.query(Filling).filter(
            Filling.id == filling_id, Filling.user_id == current_user.id).first()

        if filling is None or filling.status == 'completed':
            return redirect(url_for("filling.list"))

        question = db.session.query(Question).filter(
            Question.id == filling.question_id, Question.survey_id == filling.survey_id, Question.status == 'active').first()
        question.filling_id = filling_id
        question.is_last = filling.is_last
    except:
        db.session.rollback()
        flash('Compilazione inesistente!')

    return render_template("fillings/question.html", question=question)


@bp.route('/<int:filling_id>/save', methods=['GET', 'POST'])
@login_required
@requires_roles('panelist')
def save(filling_id):
    try:
        if request.method == 'POST':
            type = request.form['type']
            db = DB('panelist')
            filling = db.session.query(Filling).filter(
                Filling.id == filling_id, Filling.user_id == current_user.id).first()

            if type == 'radio':
                answer_id = request.form['answer']
                response = Response(type=type, survey_id=filling.survey_id,
                                    user_id=current_user.id, question_id=filling.question_id, answer_id=answer_id, filling_id=filling.id)

                db.session.add(response)

            elif type == 'multiple':
                responses = []
                values = dict(request.form.lists())

                for answer_id in values['answer']:
                    responses.append(Response(type=type, survey_id=filling.survey_id,
                                              user_id=current_user.id, question_id=filling.question_id, answer_id=answer_id, filling_id=filling.id))

                db.session.add_all(responses)

            elif type == 'text':
                response_text = request.form['response']
                response = Response(type=type, survey_id=filling.survey_id,
                                    user_id=current_user.id, question_id=filling.question_id, response=response_text, filling_id=filling.id)

                db.session.add(response)

            if filling.is_last and filling.status == 'incomplete':
                filling.status = 'completed'

                db.session.commit()

                return redirect(url_for("filling.list"))

            else:
                question_ids = []
                for question in filling.survey.questions:
                    question_ids.append(question.id)

                next_id_pos = question_ids.index(filling.question_id)
                next_question_id = question_ids[next_id_pos + 1] if len(
                    question_ids) > next_id_pos else question_ids[next_id_pos]
                is_last = len(question_ids) - \
                    1 == question_ids.index(next_question_id)

                filling.question_id = next_question_id
                filling.is_last = is_last

                db.session.commit()
    except:
        db.session.rollback()
        flash('Risposta non valida!')

    return redirect(url_for("filling.get", filling_id=filling.id))
