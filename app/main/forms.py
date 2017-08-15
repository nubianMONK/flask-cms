from urllib.parse import urlparse, urljoin
from flask import request, url_for, redirect
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, HiddenField,PasswordField, TextAreaField
from wtforms.validators import EqualTo, InputRequired, Length, ValidationError, URL, Required, Email
from wtforms.fields.html5 import EmailField

## Helper functions
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target



class RedirectForm(Form):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))



class LoginForm(Form):
    previous_page = HiddenField()
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.previous_page.data:
            self.previous_page = request.referrer or ''


    username = StringField('Username', [InputRequired('You did not provide a username.'), Length(max=80, message='Sorry, the max length of a username is 80.')])
    password = PasswordField('password', [InputRequired('You did not provide a password.')])
    submit_login = SubmitField('Log in')
    submit_forgot_password = SubmitField('Forgot Password')


class SignUp(Form):
    username = StringField('Username', [InputRequired('You did not provide a username.'), Length(max=80, message='Sorry, the max length of a username is 80.')])
    email_address = EmailField('Email Address', [InputRequired('Please enter your email address.'), Email()],)
    password = PasswordField('New Password', [Required(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Re-enter Password')
    form_submit = SubmitField('Save')

class Setting(Form):
    username = StringField('Username', [InputRequired('You did not provide a username.'), Length(max=80, message='Sorry, the max length of a username is 80.')])
    #email_address = EmailField('Email Address', [InputRequired('Please enter your email address.'), Email()],)
    email_address = EmailField('Email Address')
    password = PasswordField('Old Password', [InputRequired('You did not provide your existing password.')])
    new_password = PasswordField('New Password', [InputRequired('You did not provide a new password.')])
    form_submit = SubmitField('Save')

class AdminContentPageNew(Form):

    title = StringField('Title', [InputRequired('You did not provide a title.'), Length(max=80, message='Sorry, the max length of a title is 80.')])
    payload = TextAreaField('Content', [InputRequired('You did not provide content.')])
    author = StringField('Author', [InputRequired('You did not provide a name.'), Length(max=80, message='Sorry, the max length of an author is 80.')])
    tag = StringField('Tag', [InputRequired('You did not provide a tag/s.')])
    form_submit = SubmitField('Submit Button')

class AdminContentPageEdit(Form):
    title = StringField('Title')
    payload = TextAreaField('Content')
    author = StringField('Author')
    tag = StringField('Tag')
    form_submit = SubmitField('Update')
