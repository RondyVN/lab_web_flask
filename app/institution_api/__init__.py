from flask import Blueprint

api_teacher_blueprint = Blueprint('api/chuiko', __name__, template_folder="templates")

from . import views