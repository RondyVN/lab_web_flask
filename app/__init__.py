from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

bcrypt = Bcrypt()


def create_app(config_name = 'default'):
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        # Imports
        from .main_bp import main_bp
        app.register_blueprint(main_bp, url_prefix='/')

        from .auth import auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

        from .form_cabinet import cabinet_blueprint
        app.register_blueprint(cabinet_blueprint, url_prefix='/regcabinet')

        from .institution import inst_blueprint
        app.register_blueprint(inst_blueprint, url_prefix='/institution')

        from .posts import post_blueprint
        app.register_blueprint(post_blueprint, url_prefix='/post')

        from .api import api_blueprint
        app.register_blueprint(api_blueprint, url_prefix='/api')

        from .exz import api_teacher_blueprint
        app.register_blueprint(api_teacher_blueprint, url_prefix='/api/chuiko')

        from commands import command_blueprint
        app.register_blueprint(command_blueprint)

        return app
