from flask import Blueprint, render_template, flash, session, redirect, url_for
from .forms import DataForm, Form
from .function import validations, write_json
import json

cabinet_blueprint = Blueprint('cabinet', __name__, template_folder="templates/form_cabinet")

# Lab4
@cabinet_blueprint.route("/form", methods=['GET', 'POST'])
def form():
    form = Form()
    flash('password is password or secret')
    if form.validate_on_submit():
        return f'The username is {form.username.data}. The password is {form.password.data}'

    return render_template('form.html', form_f=form)


# lab5-6
@cabinet_blueprint.route("/register_cabinet", methods=['GET', 'POST'])
def register_cabinet():

    form = DataForm()
    validations(form)
    if form.validate_on_submit():
        session['email'] = form.email.data
        write_json(form)
        flash('User has been written in json file')
        return redirect(url_for('cabinet.register_cabinet'))

    try:
        sesiya = session['email']

    except:
        return render_template('start.html', form=form)

    with open('data.json') as f:
        data_files = json.load(f)

    form.email.data = session['email']
    form.number.data = data_files[sesiya]['number']
    form.pin.data = data_files[sesiya]['pin']
    form.year.data = data_files[sesiya]['year']
    form.serial.data = data_files[sesiya]['serial']
    form.number.data = data_files[sesiya]['number_doc']

    return render_template('start.html', form=form)