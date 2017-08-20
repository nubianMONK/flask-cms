from flask import render_template, request, redirect, flash, url_for, Markup, session, current_app
from .. import db
# from flask import Flaskapp
from ..models import Content
from ..models import Tag
from ..models import User
from .import main
from .forms import LoginForm, SignUp, Setting, AdminContentPageNew, AdminContentPageEdit
from functools import wraps
from flask_session import Session
import markdown
import re

# from flask_bootstrap import Bootstrap
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf.csrf import CsrfProtect


# app.config.from_object('config')


#db = SQLAlchemy(app)

#bootstrap = Bootstrap(app)
# CsrfProtect(app)
#cms_session = Session
#cms_flask_session = Session(app)
# Session(app)


# Helper functions

def all_contents():
    return db.session.query(Content).all()


def one_content(id):
    return db.session.query(Content).filter_by(content_id=id).one()


def get_user(username):
    return db.session.query(User).filter_by(user_name=username).one_or_none()


def is_admin(username):
    if username == current_app.config['USERNAME']:
        return True
    else:
        return False


def add_tag(tag_string):
    tag_list = tag_string.split(',')
    return tag_list


def delete_tags(content_id, tag_list):
    content = one_content(content_id)

    for tag in tag_list:
        tagRow = db.session.query(Tag).filter_by(tag_name=tag).one()
        content.content_tags.remove(tagRow)
    # tag_list = set(tag_list)
    # for tag in content.content_tags:
    #     if tag.tag_name in tag_list:
    #         content.content_tags.remove(tag)
    db.session.commit()


def insert_tags(content_id, tag_list):
    content = one_content(content_id)
    for tag in tag_list:
        tagRow = db.session.query(Tag).filter_by(tag_name=tag).one_or_none()
        if tagRow is None:
            tagRow = Tag(tag)
        content.content_tags.append(tagRow)
    db.session.commit()


def tag_by_content(id):
    tags = db.session.query(Tag).filter(
        Tag.contents.any(Content.content_id == id)).all()
    # alternate method = tags = Content.query.filter_by(content_id=id).first().content_tags
    return tags


def verify_email(email_to_verify):

    match = re.match(
        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email_to_verify)
    if match == None:
        return False
    else:
        return True

# @app.route('/content', methods=['GET', 'POST'])
# def content():
#     if request.method == 'GET':
#         contents = all_contents()
#         return render_template('contentOne.html', contents=contents)


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('.login'))
    return wrap


@main.route('/admin_content_page_new', methods=['GET', 'POST'])
@login_required
def admin_content_page_new():
    form = AdminContentPageNew(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_content_page = Content(
                form.title.data, form.payload.data, form.author.data)
            db.session.add(new_content_page)
            tags = add_tag(form.tag.data)
            for tag in tags:
                new_tag = Tag(tag)
                new_content_page.content_tags.append(new_tag)

            db.session.commit()
            flash('New Content saved.')
            return redirect(url_for('.admin_index'))
    return render_template('admin_content_page_new.html', form=form)


@main.route('/admin_content_page_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_content_page_edit(id):
    form = AdminContentPageEdit(request.form)
    content_page = one_content(id)

    # returns a list of current tag objects
    tags = tag_by_content(id)
    current_tag_list = []
    tags_to_insert = []
    tags_to_delete = []
    tags_to_update = []

    for tag in tags:
        # building a list of current tags
        current_tag_list.append(tag.tag_name)

    # a string of current tags
    current_tag_string = ','.join(current_tag_list)

    if request.method == 'POST':
        if form.validate_on_submit():

            updated_title = form.title.data
            updated_payload = Markup(markdown.markdown(form.payload.data))
            updated_payload = form.payload.data
            updated_author = form.author.data
            updated_tag = add_tag(form.tag.data)
            updated_tag = [v.strip().lower() for v in updated_tag]
            updated_content_page = db.session.query(Content).filter_by(content_id=id).update(
                {
                    "title": updated_title, "payload": updated_payload, "author": updated_author

                }
            )

            for tag in current_tag_list:
                if tag not in updated_tag:
                    tags_to_delete.append(tag)

            if len(tags_to_delete) > 0:
                delete_tags(id, tags_to_delete)

            for tag in updated_tag:
                if tag not in current_tag_list:
                    tags_to_insert.append(tag)

            if len(tags_to_insert) > 0:
                insert_tags(id, tags_to_insert)

            db.session.commit()
            flash('Updated Content saved.')
            return redirect(url_for('.content', id=id))

    elif request.method == 'GET':
        form.title.data = content_page.title
        form.payload.data = content_page.payload
        form.author.data = content_page.author
        form.tag.data = current_tag_string
        return render_template('admin_content_page_edit.html', form=form, content_page=content_page, tag_string=current_tag_string)


@main.route('/admin_index', methods=['GET'])
@login_required
def admin_index():
    if request.method == 'GET':
        contents = all_contents()
        return render_template('admin_index.html', contents=contents, session=session)


@main.route('/content/', defaults={'id': ''}, methods=['GET'])
@main.route('/content/<int:id>', methods=['GET'])
#@app.route('/content/<int:id>/<path:path>', methods=['GET'])
def content(id):
    if request.method == 'GET':
        if id:
            single_content = one_content(id)
            single_content = {
                "title": single_content.title, "payload": single_content.payload, "author": single_content.author, "content_id": single_content.content_id
            }

            tags = tag_by_content(id)
            single_content["payload"] = Markup(
                markdown.markdown(single_content["payload"]))
            return render_template('content.html', single_content=single_content, tags=tags)
        else:
            contents = all_contents()
            #tags = tag_by_content(path)
            return render_template('contents.html', contents=contents)


# @app.route('/content/<int:id>', methods=['GET'])
# def content(id):
#     if request.method == 'GET':
#
#         single_content = one_content(id)
#         single_content = {
#           "title": single_content.title
#             , "payload": single_content.payload
#             , "author": single_content.author
#             , "content_id": single_content.content_id
#         }
#
#         tags = tag_by_content(id)
#         single_content["payload"] = Markup(markdown.markdown(single_content["payload"]))
#         return render_template('content.html', single_content=single_content, tags=tags )


@main.route('/login', methods=['GET', 'POST'])
def login():
    #previous_page = request.referrer
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user = get_user(form.username.data)
            if login_user.user_name != form.username.data or login_user.password != form.password.data:
                # if form.username.data != app.config['USERNAME'] or form.password.data != app.config['PASSWORD']:
                flash('Invalid Credentials. Please try again')

            else:
                session['logged_in'] = True
                session['name'] = form.username.data
                session['admin'] = is_admin(form.username.data)
                flash(form.previous_page)
                return redirect(form.previous_page)

    return render_template('login.html', form=form)


@main.route('/logout', methods=['POST'])
def logout():
    """Logout route."""

    session.clear()
    return redirect(url_for('.login'))


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUp(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_sign_up = User(form.username.data,
                               form.email_address.data, form.password.data)
            db.session.add(new_sign_up)
            db.session.commit()
            flash('successfully signed up.')
            return redirect(url_for('.login'))
    return render_template('signup.html', form=form)


@main.route('/setting', methods=['GET', 'POST'])
def setting():
    form = Setting(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            is_valid_email = verify_email(form.email_address.data)
            user_settings = get_user(form.username.data)
            if user_settings:

                if user_settings.password == form.password.data:
                    user_settings.password = form.new_password.data
                    if form.email_address.data and is_valid_email:
                        user_settings.email_address = form.email_address.data

                    db.session.commit()
                    flash('Password, successfully saved.')
                    return render_template('content.html')

            else:
                flash('invalid user, please input a valid user.')
    return render_template('settings.html', form=form)
