import csv

from flask import Blueprint, request, render_template, redirect, url_for, send_file
from flask_login import current_user, login_required
from sqlalchemy import text

from ds.helpers.auth import requires_roles
from ds.models.filling import Filling
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

    ###############################################################
    # Get Survey by ID in order to set export data filename
    ###############################################################
    survey = db.session.query(Survey).filter(Survey.id == id).first()
    filename = f'{survey.title}.csv'.replace(' ', '')

    ###############################################################
    # Fetch all completed fillings data
    ###############################################################
    responses = db.session.execute(
        text("SELECT                                                                                        \
                    r.user_id AS user_id,                                                                   \
                    JSON_AGG(                                                                               \
                        JSON_BUILD_OBJECT(                                                                  \
                            'question_id', q.id,                                                            \
                            'question_order', q.seq,                                                        \
                            'question_type', q.type,                                                        \
                            'options_number',                                                               \
                                (SELECT COUNT(*)                                                            \
                                FROM questions q1 JOIN answers a1 on q1.id=a1.question_id                   \
                                WHERE q1.id=q.id AND a1.status=:answer_status),                             \
                            'question', q.title,                                                            \
                            'answer', coalesce(a.answer, r.response)                                        \
                        )                                                                                   \
                    )                                                                                       \
            FROM (responses r JOIN fillings f ON (r.filling_id = f.id AND f.status = :filling_status))      \
                    JOIN questions q ON r.question_id=q.id LEFT OUTER JOIN answers a ON r.answer_id = a.id  \
            WHERE r.survey_id = :survey_id GROUP BY r.user_id"),
        {
            "answer_status": 'active',
            "filling_status": 'completed',
            "survey_id": id
        }).fetchall()

    ##################################################################
    # Setting responses data in csv file
    ##################################################################
    header = []
    data = []
    header.append('user_id')
    for x in responses:
        data.append([x[0]])

    for question in survey.questions:
        header.append(f'question_{survey.questions.index(question) + 1}')
        for x in data:
            x.append(question.title)

        if question.type == 'multiple':
            for answer in question.answers:
                header.append(f'answer_{question.answers.index(answer) + 1}')
            for x in responses:
                uid = x[0]
                for d in data:
                    if d[0] == uid:
                        rs = x[1]
                        m_res = [r for r in rs if r['question_id']
                                 == question.id]
                        opts_num = m_res[0]['options_number']
                        for mr in m_res:
                            d.append(mr['answer'])

                        for _ in range(opts_num - len(m_res)):
                            d.append(" ")
        else:
            header.append(f'answer_{survey.questions.index(question) + 1}')
            for x in responses:
                uid = x[0]
                for d in data:
                    if d[0] == uid:
                        rs = x[1]
                        response = [
                            r for r in rs if r['question_id'] == question.id][0]
                        d.append(response['answer'])

    ##################################################################
    # Creating csv file and writing header and data rows
    ##################################################################
    with open(f'exports/{filename}', 'w', newline='\n', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        spamwriter.writerow(header)
        spamwriter.writerows(data)

    ##################################################################
    # Send csv file as response attachment
    ##################################################################
    return send_file(f'../exports/{filename}',
                     mimetype='text/csv',
                     attachment_filename=f'{filename}',
                     as_attachment=True)
