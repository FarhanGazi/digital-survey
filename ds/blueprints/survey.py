import csv
from ds.models.filling import Filling
from flask import Blueprint, request, render_template, redirect, url_for, send_file
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
    db = DB('ds')
    surveys = db.session.query(Survey).order_by(Survey.id.asc()).all()
    return render_template("admin/surveys/list.html", surveys=surveys)


@bp.route('/<int:id>', methods=['GET'])
@login_required
@requires_roles('admin')
def details(id):
    db = DB('ds')
    survey = db.session.query(Survey).filter(Survey.id == id).first()
    completed_fillings = db.session.query(Filling.user_id).filter(
        Filling.survey_id == id, Filling.status == 'completed').group_by(Filling.user_id).count()
    survey.completed_fillings = completed_fillings

    return render_template("admin/surveys/details.html", survey=survey)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def create():
    if request.method == 'POST':
        title = request.form["title"]
        status = request.form["status"]
        description = request.form["description"]
        db = DB('ds')
        new_surevy = Survey(title=title, description=description,
                            status=status, user_id=current_user.id)
        db.session.add(new_surevy)
        db.session.commit()
        return redirect(url_for("survey.details", id=new_surevy.id))

    elif request.method == 'GET':
        return render_template("admin/surveys/create.html")


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def update(id):
    if request.method == 'POST':
        title = request.form["title"]
        status = request.form["status"]
        description = request.form["description"]
        db = DB('ds')
        survey = db.session.query(Survey).filter(Survey.id == id).first()
        survey.title = title
        survey.status = status
        survey.description = description
        db.session.commit()
        return redirect(url_for("survey.details", id=survey.id))

    elif request.method == 'GET':
        db = DB('ds')
        survey = db.session.query(Survey).filter(Survey.id == id).first()
        return render_template("admin/surveys/update.html", survey=survey)


@bp.route('/<int:id>/delete')
@login_required
@requires_roles('admin')
def delete(id):
    db = DB('ds')
    survey = db.session.query(Survey).filter(Survey.id == id).first()
    db.session.delete(survey)
    db.session.commit()
    return redirect(url_for("survey.list"))


@bp.route('/<int:id>/export')
@login_required
@requires_roles('admin')
def export(id):
    db = DB('ds')
    survey = db.session.query(Survey).filter(Survey.id == id).first()
    filename = f'{survey.title}.csv'.replace(' ', '')

    with open(f'exports/{filename}', 'w', newline='\n', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    return send_file(f'../exports/{filename}',
                     mimetype='text/csv',
                     attachment_filename=f'{filename}',
                     as_attachment=True)

###################################################################################
# DATA EXPORT QUERY
#
# explain analyze select user_id,
# json_agg(json_build_object('question_id', questions.id, 'question_order',
# questions.seq, 'question_type', questions.type, 'options_number',
# (select count(*) from questions q1 join answers a1 on q1.id=a1.question_id where q1.id=questions.id and a1.status='active'),
# 'question', questions.title, 'answer', coalesce(answers.answer, responses.response))) from responses join questions on
# responses.question_id = questions.id left outer join answers on responses.answer_id = answers.id where responses.survey_id = 1 group by responses.user_id
#
###################################################################################
