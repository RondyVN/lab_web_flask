from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisSecretKey'


class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')


@app.route("/form")
def start():
    form = LoginForm()
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
