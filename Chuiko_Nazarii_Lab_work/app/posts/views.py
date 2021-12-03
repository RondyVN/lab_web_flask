from flask import url_for, render_template, redirect
from flask_login import login_required
from .models import Posts, Category
from flask import url_for, render_template, flash, request, redirect, abort, current_app
from .. import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from .forms import CreatePostForm


from . import post_blueprint
from PIL import Image


@post_blueprint.route('/', methods=['GET', 'POST'])
def view_post():
    all_posts = Posts.query.all()
    return render_template('post.html', posts=all_posts)


@post_blueprint.route('/<pk>', methods=['GET', 'POST'])
def view_detail(pk):
    get_post = Posts.query.get_or_404(pk)
    return render_template('detail_post.html', pk=get_post)


@post_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePostForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            image = picture_file
        else:
            image = 'postdefault.jpg'

        post = Posts(title=form.title.data, text=form.text.data, type=form.type.data, image_file=image,
                     post_id=current_user.id, category_id=form.category.data)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('post.view_post'))

    return render_template('create_post.html', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/posts_pics', picture_fn)
    output_size = (250, 250)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@post_blueprint.route('/delete/<pk>', methods=['GET', 'POST'])
@login_required
def delete_post(pk):
    get_post = Posts.query.get_or_404(pk)
    if current_user.id == get_post.post_id:
        db.session.delete(get_post)
        db.session.commit()
        return redirect(url_for('post.view_post'))

    flash('This is not your post', category='warning')
    return redirect(url_for('post.view_detail', pk=pk))


@post_blueprint.route('/update/<pk>', methods=['GET', 'POST'])
@login_required
def update_post(pk):
    get_post = Posts.query.get_or_404(pk)
    if current_user.id != get_post.post_id:
        flash('This is not your post', category='warning')
        return redirect(url_for('post.view_detail', pk=pk))

    form = CreatePostForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            get_post.image_file = picture_file

        get_post.title = form.title.data
        get_post.text = form.text.data
        get_post.type = form.type.data
        get_post.enabled = form.enabled.data
        get_post.category_id = form.category.data

        db.session.add(get_post)
        db.session.commit()

        flash('You post has been update', category='access')
        return redirect(url_for('post.view_detail', pk=pk))

    form.title.data = get_post.title
    form.text.data = get_post.text
    form.type.data = get_post.type
    form.enabled.data = get_post.enabled
    form.category.data = get_post.category_id

    return render_template('update_post.html', form=form)


@post_blueprint.route('/category', methods=['GET', 'POST'])
def get_category():
    category = Category.query.all()
    return render_template('category.html', category=category)


@post_blueprint.route('/category/<pk>', methods=['GET', 'POST'])
def view_category_post(pk):
    all_posts = Posts.query.filter_by(category_id=pk)
    return render_template('post.html', posts=all_posts)


