from re import U
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from ds.helpers.auth import requires_roles
from ds.models.user import User
from configs.sqladb import DB

bp = Blueprint("user", __name__, url_prefix="/users")


@bp.route('/', methods=['GET'])
@login_required
@requires_roles('admin')
def list():
    db = DB('ds')
    users = db.session.query(User).order_by(User.id.asc()).all()
    return render_template("admin/users/list.html", users=users)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def create():
    if request.method == 'POST':
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        db = DB('ds')
        new_user = User(name=name, surname=surname, email=email, role=role, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("user.list"))

    elif request.method == 'GET':
        return render_template("admin/users/create.html")


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def update(id):
    if request.method == 'POST':
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        db = DB('ds')
        user = db.session.query(User).filter(User.id == id).first()
        user.name = name
        user.surname = surname
        user.email = email
        user.password = password
        user.role = role
        db.session.commit()

        return redirect(url_for("user.list"))

    elif request.method == 'GET':
        db = DB('ds')
        user = db.session.query(User).filter(User.id == id).first()
        return render_template("admin/users/update.html", user=user)


@bp.route('/<int:id>/delete')
@login_required
@requires_roles('admin')
def delete(id):
    db = DB('ds')
    user = db.session.query(User).filter(User.id == id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("user.list"))
