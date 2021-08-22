from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required

from ds.helpers.auth import requires_roles
from ds.models.question import Question
from configs.sqladb import DB

bp = Blueprint("question", __name__,
               url_prefix="/surveys/<int:survey_id>/questions")


@bp.route('/<int:question_id>', methods=['GET'])
@login_required
@requires_roles('admin')
def details(survey_id, question_id):
    try:
        db = DB('admin')
        question = db.session.query(Question).filter(
            Question.id == question_id, Question.survey_id == survey_id).first()

        data = {
            'survey_id': survey_id,
            'question': question
        }
        return render_template("admin/questions/details.html", data=data)
    except:
        db.session.rollback()
        flash('Domanda inesistente!')
        return redirect(url_for("survey.details", id=survey_id))


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def create(survey_id):
    if request.method == 'POST':
        try:
            type = request.form["type"]
            title = request.form["title"]
            seq = request.form["seq"]
            status = request.form["status"]
            description = request.form["description"]

            db = DB('admin')
            new_question = Question(title=title, description=description,
                                    type=type, seq=seq, status=status, survey_id=survey_id)
            db.session.add(new_question)
            db.session.commit()

            return redirect(url_for("question.details", survey_id=survey_id, question_id=new_question.id))
        except:
            db.session.rollback()
            flash('Alcuni campi sono invalidi!')
            return redirect(url_for("question.create", survey_id=survey_id))

    elif request.method == 'GET':
        try:
            db = DB('admin')
            questions_count = db.session.query(Question).filter(
                Question.survey_id == survey_id).count() + 1

            data = {
                'survey_id': survey_id,
                'total': questions_count
            }
            return render_template("admin/questions/create.html", data=data)

        except:
            db.session.rollback()
            flash('Questionario inesistente!')
            return redirect(url_for("survey.list"))


@bp.route('/<int:question_id>/update', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def update(survey_id, question_id):
    if request.method == 'POST':
        try:
            type = request.form["type"]
            title = request.form["title"]
            seq = request.form["seq"]
            status = request.form["status"]
            description = request.form["description"]

            db = DB('admin')
            question = db.session.query(Question).filter(
                Question.id == question_id, Question.survey_id == survey_id).first()
            question.type = type
            question.title = title
            question.seq = seq
            question.status = status
            question.description = description
            db.session.commit()

            return redirect(url_for("question.details", survey_id=survey_id, question_id=question_id))

        except:
            db.session.rollback()
            flash('Alcuni campi non sono validi!')
            return redirect(url_for("question.update", survey_id=survey_id, question_id=question_id))

    elif request.method == 'GET':
        try:
            db = DB('admin')
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

        except:
            db.session.rollback()
            flash('Domanda inesistente!')
            return redirect(url_for("survey.list"))


@bp.route('/<int:question_id>/delete')
@login_required
@requires_roles('admin')
def delete(survey_id, question_id):
    try:
        db = DB('admin')
        question = db.session.query(Question).filter(
            Question.id == question_id).first()
        db.session.delete(question)
        db.session.commit()
    except:
        db.session.rollback()
        flash('Domanda inesistente!')

    return redirect(url_for("survey.details", id=survey_id))
