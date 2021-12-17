from flask import Blueprint

inst_blueprint = Blueprint('inst', __name__, template_folder="templates/institution")

from . import views
