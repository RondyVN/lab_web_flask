from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Regexp, EqualTo, DataRequired, ValidationError
from .models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('A username is required'), Length(min=4, max=14,
                                                                                                   message='Name must have greater 4 symbol and least 14 symbol'),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Username must have only letters, numbers, dots or underscores')])
    email = StringField('Email', validators=[InputRequired('Email is required'),
                                             Regexp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                                                    message='Invali Email')])
    password1 = PasswordField('Password', validators=[InputRequired('Password is required'),
                                                      Length(min=6, message='Must be at least 6')])
    password2 = PasswordField('Repeat the password', validators=[InputRequired('Password is required'),
                                                                 Length(min=6, message='Must be at least 6'),
                                                                 EqualTo('password1')])
    submit = SubmitField(label=(''))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Regexp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('')
    submit = SubmitField(label=(''))


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[InputRequired('Email is required'),
                                             Regexp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                                                    message='Invali Email')])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is take. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one')
