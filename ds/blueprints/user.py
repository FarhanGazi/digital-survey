from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from ds.helpers.auth import requires_roles
from ds.models.user import User
from configs.sqladb import DB

bp = Blueprint("user", __name__, url_prefix="/users")


######################################################################################
# USERS LIST
#
# Endpoint: /users/
# Parameteres: -
# GET all users
######################################################################################
@bp.route('/', methods=['GET'])
@login_required
@requires_roles('admin')
def list():
    try:
        db = DB('admin')
        users = db.session.query(User).filter(
            User.id != current_user.id).order_by(User.id.asc()).all()
    except:
        db.session.rollback()
        flash('Qualcosa è andato storto!')

    return render_template("admin/users/list.html", users=users)


######################################################################################
# USERS CREATE
#
# Endpoint: /users/create
# Parameteres: -
# GET user creation FORM and creates user in POST
######################################################################################
@bp.route('/create', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def create():
    if request.method == 'POST':
        try:
            name = request.form["name"]
            surname = request.form["surname"]
            email = request.form["email"]
            password = request.form["password"]
            role = request.form["role"]
            db = DB('admin')
            new_user = User(name=name, surname=surname,
                            email=email, role=role, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("user.list"))

        except:
            db.session.rollback()
            flash('Alcuni campi non sono valdi!')
            return redirect(url_for("user.create"))

    elif request.method == 'GET':
        return render_template("admin/users/create.html")


######################################################################################
# USERS UPDATE
#
# Endpoint: /<int:id>/update
# Parameteres: id
# GET user upadte FORM with its data and updates user in POST
######################################################################################
@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def update(id):
    if request.method == 'POST':
        try:
            name = request.form["name"]
            surname = request.form["surname"]
            email = request.form["email"]
            password = request.form["password"]
            role = request.form["role"]

            db = DB('admin')
            user = db.session.query(User).filter(User.id == id).first()
            user.name = name
            user.surname = surname
            user.email = email
            user.password = password
            user.role = role
            db.session.commit()

            return redirect(url_for("user.list"))

        except:
            db.session.rollback()
            flash('Alcuni campi non sono valdi!')
            return redirect(url_for("user.update", id=id))

    elif request.method == 'GET':
        try:
            db = DB('admin')
            user = db.session.query(User).filter(User.id == id).first()
            return render_template("admin/users/update.html", user=user)

        except:
            db.session.rollback()
            flash('Utente inesistente!')
            return redirect(url_for("user.list"))


######################################################################################
# USERS DELETE
#
# Endpoint: /<int:id>/delete
# Parameteres: id
# DELETE user by ID
######################################################################################
@bp.route('/<int:id>/delete')
@login_required
@requires_roles('admin')
def delete(id):
    try:
        db = DB('admin')
        user = db.session.query(User).filter(User.id == id).first()
        db.session.delete(user)
        db.session.commit()
    except:
        db.session.rollback()
        flash('Utente inesistente!')

    return redirect(url_for("user.list"))
