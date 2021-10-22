from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, AnyOf


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisSecretKey'


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is required'), Length(min=5, max=10, message='Must be at least 5 and at most 10 characters')])
    password = PasswordField('password', validators=[InputRequired('Password is required'), AnyOf(values=['password', 'secret'])])


@app.route("/form", methods=['GET', 'POST'])
def form():
    form = LoginForm()

    if form.validate_on_submit():
        return f'The username is {form.username.data}. The password is {form.password.data}'

    return render_template('form.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
