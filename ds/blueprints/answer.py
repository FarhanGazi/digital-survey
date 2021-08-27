from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required

from ds.helpers.auth import requires_roles
from ds.models.answer import Answer
from configs.sqladb import DB

bp = Blueprint("answer", __name__,
               url_prefix="/surveys/<int:survey_id>/questions/<int:question_id>/answers")


######################################################################################
# ANSWER CREATE
#
# Endpoint: /surveys/<int:survey_id>/questions/<int:question_id>/answer/create
# Parameteres: survey_id, question_id
# Method which creates Answers when in POST and shows Answer creation FROM when in GET
######################################################################################
@bp.route('/create', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def create(survey_id, question_id):
    if request.method == 'POST':
        try:
            answer = request.form['answer']
            status = request.form['status']

            db = DB('admin')
            new_answer = Answer(answer=answer, status=status,
                                question_id=question_id)
            db.session.add(new_answer)
            db.session.commit()

            return redirect(url_for("question.details", survey_id=survey_id, question_id=question_id))
        except:
            db.session.rollback()
            flash('Alcuni campi non sono validi!')
            return redirect(url_for("question.create", survey_id=survey_id, question_id=question_id))

    elif request.method == 'GET':
        data = {
            'survey_id': survey_id,
            'question_id': question_id
        }
        return render_template("admin/answers/create.html", data=data)


######################################################################################
# ANSWER UPDATE
#
# Endpoint: /surveys/<int:survey_id>/questions/<int:question_id>/answer/update
# Parameteres: survey_id, question_id, answer_id
# Method which updates Answers when in POST and shows Answer creation FROM when in GET
######################################################################################
@bp.route('/<int:answer_id>/update', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def update(survey_id, question_id, answer_id):
    if request.method == 'POST':
        try:
            text = request.form['answer']
            status = request.form['status']

            db = DB('admin')
            answer = db.session.query(Answer).filter(
                Answer.id == answer_id, Answer.question_id == question_id).first()

            answer.answer = text
            answer.status = status

            db.session.commit()
            return redirect(url_for("question.details", survey_id=survey_id, question_id=question_id))

        except:
            db.session.rollback()
            flash('Alcuni campi non sono validi!')
            return redirect(url_for("question.update", survey_id=survey_id, question_id=question_id, answer_id=answer_id))

    elif request.method == 'GET':
        db = DB('admin')
        answer = db.session.query(Answer).filter(
            Answer.id == answer_id, Answer.question_id == question_id).first()
        data = {
            'survey_id': survey_id,
            'question_id': question_id,
            'answer': answer
        }
        return render_template("admin/answers/update.html", data=data)


######################################################################################
# ANSWER DELETE
#
# Endpoint: /surveys/<int:survey_id>/questions/<int:question_id>/answer/delete
# Parameteres: survey_id, question_id, answer_id
# Method to delete Answers
########################################################################################
@bp.route('/<int:answer_id>/delete')
@login_required
@requires_roles('admin')
def delete(survey_id, question_id, answer_id):
    try:
        db = DB('admin')
        answer = db.session.query(Answer).filter(
            Answer.id == answer_id).first()
        db.session.delete(answer)
        db.session.commit()
    except:
        db.session.rollback()
        flash('Qualcosa è andato storto!')

    return redirect(url_for("question.details", survey_id=survey_id, question_id=question_id))
