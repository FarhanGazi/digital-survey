from datetime import date
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_required

from ds.helpers.auth import requires_roles
from ds.models.user import User
from ds.models.survey import Survey
from ds.models.question import Question
from configs.sqladb import DB

bp = Blueprint("question", __name__,
               url_prefix="/surveys/<int:survey_id>/questions")


@bp.route('/<int:question_id>', methods=['GET'])
@login_required
@requires_roles('admin')
def details(survey_id, question_id):
    db = DB('ds')
    question = db.session.query(Question).filter(
        Question.id == question_id, Question.survey_id == survey_id).first()

    data = {
        'survey_id': survey_id,
        'question': question
    }
    return render_template("admin/questions/details.html", data=data)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def create(survey_id):
    if request.method == 'POST':
        type = request.form["type"]
        title = request.form["title"]
        seq = request.form["seq"]
        status = request.form["status"]
        description = request.form["description"]

        db = DB('ds')
        new_question = Question(title=title, description=description,
                                type=type, seq=seq, status=status, survey_id=survey_id)
        db.session.add(new_question)
        db.session.commit()

        return redirect(url_for("question.details", survey_id=survey_id, question_id=new_question.id))

    elif request.method == 'GET':
        db = DB('ds')
        questions_count = db.session.query(Question).filter(
            Question.survey_id == survey_id).count() + 1

        data = {
            'survey_id': survey_id,
            'total': questions_count
        }
        return render_template("admin/questions/create.html", data=data)


@bp.route('/<int:question_id>/update', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def update(survey_id, question_id):
    if request.method == 'POST':
        type = request.form["type"]
        title = request.form["title"]
        seq = request.form["seq"]
        status = request.form["status"]
        description = request.form["description"]

        db = DB('ds')
        question = db.session.query(Question).filter(Question.id == question_id, Question.survey_id == survey_id).first()
        question.type = type
        question.title = title
        question.seq = seq
        question.status = status
        question.description = description
        db.session.commit()

        return redirect(url_for("question.details", survey_id=survey_id, question_id=question.id))

    elif request.method == 'GET':
        db = DB('ds')
        question = db.session.query(Question).filter(
            Question.id == question_id, Question.survey_id == survey_id).first()

        questions_count = db.session.query(Question).filter(
            Question.survey_id == survey_id).count()

        data = {
            'survey_id': survey_id,
            'total': questions_count,
            'question': question
        }
        return render_template("admin/questions/update.html", data=data)


@bp.route('/<int:question_id>/delete')
@login_required
@requires_roles('admin')
def delete(survey_id, question_id):
    return
