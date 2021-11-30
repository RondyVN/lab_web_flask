from flask import url_for, render_template, redirect
from flask_login import login_required
from ..auth.models import Posts
from flask import url_for, render_template, flash, request, redirect, abort, current_app
from .. import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from .forms import CreatePostForm
from sqlalchemy import exc

from PIL import Image
from datetime import datetime

from . import post_blueprint
from PIL import Image
@post_blueprint.route('/')
@login_required
def index():
    return render_template('index.html')


@post_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePostForm()
    if form.validate_on_submit:
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        post = Posts(title=form.title.data, text=form.text.data, type=form.type.data)
        print(post.title)
        print(post.text)
        print(post.type)
        print(post)

        try:
            db.session.add(post)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()


    return render_template('create_post.html', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (250, 250)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
