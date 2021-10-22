from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisSecretKey'


class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')


@app.route("/form", methods=['GET', 'POST'])
def form():
    form = LoginForm()

    if form.validate_on_submit():
        return f'The username is {form.username.data}. The password is {form.password.data}'
    
    return render_template('form.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
