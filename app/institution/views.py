from flask import url_for, render_template, flash, request, redirect, abort, current_app
from .forms import AddInstForm, CategoryForm
from . import inst_blueprint
from .models import Categoryacr, Institution
from .. import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@inst_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def view_inst():
    institution = Institution.query.order_by(Institution.name_inst).all()
    return render_template('view_inst.html', institutions=institution)


@inst_blueprint.route('/addinst', methods=['GET', 'POST'])
@login_required
def add_institution():
    form = AddInstForm()
    form.category.choices = [(category.id, category.level) for category in Categoryacr.query.all()]
    if form.validate_on_submit():
        inst = Institution(
            name_inst=form.name_inst.data,
            count_student=form.count_student.data,
            info=form.text.data,
            city=form.city.data,
            military_department=form.military_department.data,
            category_acr_id=form.category.data,
            user_id=current_user.id
        )

        db.session.add(inst)
        db.session.commit()

        return redirect(url_for('inst.view_inst'))
    return render_template('institution_add.html', form=form)


@inst_blueprint.route('/<id>', methods=['GET', 'POST'])
def detail_inst(id):
    institution = Institution.query.get_or_404(id)
    return render_template('institution_detail.html', pk=institution)


@inst_blueprint.route('/delete/<id>', methods=['GET', 'POST'])
def delete_inst(id):
    institution = Institution.query.get_or_404(id)
    if current_user.id == institution.user_id:
        db.session.delete(institution)
        db.session.commit()
        return redirect(url_for('inst.view_inst'))

    flash('This is not your post', category='warning')
    return redirect(url_for('inst.detail_inst', pk=id))


@inst_blueprint.route('/edit/<id>', methods=['GET', 'POST'])
def edit_inst(id):
    institution = Institution.query.get_or_404(id)
    if current_user.id != institution.user_id:
        flash('This is not your post', category='warning')
        return redirect(url_for('inst.detail_inst', pk=institution))

    form = AddInstForm()
    form.category.choices = [(category.id, category.level) for category in Categoryacr.query.all()]

    if form.validate_on_submit():
        institution.name_inst = form.name_inst.data
        institution.info = form.text.data
        institution.count_student = form.count_student.data
        institution.city = form.city.data
        institution.military_department = form.military_department.data
        institution.category_acr_id = form.category.data

        db.session.add(institution)
        db.session.commit()

        flash('Institution has been update', category='access')
        return redirect(url_for('inst.detail_inst', id=id))

    form.name_inst.data = institution.name_inst
    form.text.data = institution.info
    form.count_student.data = institution.count_student
    form.city.data = institution.city
    form.military_department.data = institution.military_department
    form.category.data = institution.category_acr_id

    return render_template('institution_add.html', form=form)


@inst_blueprint.route('/catacrcrud', methods=['GET', 'POST'])
def category_crud():
    form = CategoryForm()

    if form.validate_on_submit():
        category = Categoryacr(level=form.name.data)

        db.session.add(category)
        db.session.commit()
        flash('Категорія добавленна')
        return redirect(url_for('.category_crud'))

    categories = Categoryacr.query.all()
    return render_template('category_crud.html', categories=categories, form=form)


@inst_blueprint.route('/update_category/<id>', methods=['GET', 'POST'])
def update_category(id):
    category = Categoryacr.query.get_or_404(id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.level = form.name.data

        db.session.add(category)
        db.session.commit()
        flash('Категорія відредагована')
        return redirect(url_for('.category_crud'))

    form.name.data = category.level
    categories = Categoryacr.query.all()
    return render_template('category_crud.html', categories=categories, form=form)


@inst_blueprint.route('/delete_category/<id>', methods=['GET'])
@login_required
def delete_category(id):
    category = Categoryacr.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()

    flash('Category delete', category='access')
    return redirect(url_for('.category_crud'))
