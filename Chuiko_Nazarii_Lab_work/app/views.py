from flask import url_for, render_template, session, request, flash, redirect
from flask import current_app as app
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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

