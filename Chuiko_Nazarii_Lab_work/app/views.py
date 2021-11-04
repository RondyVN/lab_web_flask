from flask import Flask, url_for, render_template, session, request, flash, redirect, abort
from . import app, db
from .forms import Form, DataForm, SignUpForm, LoginForm
from .function import write_json, validations
from .models import User
import os, sys, platform, json
from datetime import datetime


# Lab3
@app.route("/blog")
def blog():
    news_dict = {
        'first day': 'I feel good',
        'Second Day': 'I feel bad',
        'Third Day': 'I happy',

    }
    return render_template("blog.html", news_dict=news_dict, sys_info=request.headers.get('User-Agent'),
                           sys=sys.version, os_name=os.name, platform=platform.system(), release=platform.release(),
                           date=datetime.now())


@app.route("/news")
def news():
    news_dict = {
        'I start study Django': 'ok',
        'Okay': 'Today nice weather',
        'tomorow': 'I walk to university',

    }
    return render_template("news.html", news_dict=news_dict, sys_info=request.headers.get('User-Agent'),
                           sys=sys.version, os_name=os.name, platform=platform.system(), release=platform.release(),
                           date=datetime.now())


@app.route("/")
def portfolio():
    return render_template("personal_portfolio.html", boolean=False, name='Nazar', error='Wrong data',
                           sys_info=request.headers.get('User-Agent'), sys=sys.version, os_name=os.name,
                           platform=platform.system(), release=platform.release(), date=datetime.now())


# Lab4
@app.route("/form", methods=['GET', 'POST'])
def form():
    form = Form()
    flash('password is password or secret')
    if form.validate_on_submit():
        return f'The username is {form.username.data}. The password is {form.password.data}'

    return render_template('form.html', form_f=form)


# lab5-6
@app.route("/register_cabinet", methods=['GET', 'POST'])
def register_cabinet():

    form = DataForm()
    validations(form)
    if form.validate_on_submit():
        session['email'] = form.email.data
        write_json(form)
        flash('User has been written in json file')
        return redirect(url_for('register_cabinet'))

    try:
        ses = session['email']
    except:
        return render_template('start.html', form=form)

    with open('data.json') as f:
        data_files = json.load(f)

    return render_template('start.html', form=form, email=ses, number=data_files[ses]['number'], year=data_files[ses]['year'], pin=data_files[ses]['pin'], serial=data_files[ses]['serial'], number_doc=data_files[ses]['number_doc'], )


# lab7
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} !', category='success')
        return redirect(url_for('login'))
    return render_template('signup.html', form_reg=form, title='Register')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_log = LoginForm()
    if form_log.validate_on_submit():
        user = User.query.filter_by(email=form_log.email.data).first()
        if user and user.verify_password(form_log.password.data):
            flash(f'You have been logged by username {user.email}!', category='success')
            return redirect(url_for('login'))
        else:
            flash('Invalid login or password!', category='warning')
            return redirect(url_for('login'))

    return render_template('login.html', form_log=form_log, title='Login')


@app.route("/users", methods=['GET', 'POST'])
def users():
    all_users = User.query.all()
    count = User.query.count()
    if count == 0:
        abort(404)
    return render_template('user_list.html', all_users=all_users, count=count)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')