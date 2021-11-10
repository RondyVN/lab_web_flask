from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

bcrypt = Bcrypt(app)

from . import views

from .auth import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from .form_cabinet import cabinet_blueprint
app.register_blueprint(cabinet_blueprint, url_prefix='/regcabinet')


