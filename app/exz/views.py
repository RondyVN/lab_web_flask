from flask import Flask, g, request, jsonify
from functools import wraps
from ..institution.models import Institution
from .. import db

from . import api_teacher_blueprint

api_username = 'admin'
api_password = 'password'


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403

    return decorated


@api_teacher_blueprint.route('/institutions', methods=['GET'])
@protected
def get_institutions():
    institutions = Institution.query.all()
    return_values = [{"id": institution.id,
                      "name_inst": institution.name_inst,
                      "info": institution.info,
                      "count_student": institution.count_student,
                      "city": institution.city,
                      "military_department": institution.military_department,
                      "category_acr_id": institution.category_acr_id} for institution in institutions]

    return jsonify({'Institution': return_values})


@api_teacher_blueprint.route('/institution/<int:id>', methods=['GET'])
@protected
def get_institution(id):
    institution = Institution.query.get_or_404(id)
    return jsonify({"id": institution.id,
                    "name_inst": institution.name_inst,
                    "info": institution.info,
                    "count_student": institution.count_student,
                    "city": institution.city,
                    "military_department": institution.military_department,
                    "category_acr_id": institution.category_acr_id})


@api_teacher_blueprint.route('/institution', methods=['POST'])
def add_institution():
    new_institution_data = request.get_json()
    institution = Institution.query.filter_by(name_inst=new_institution_data['name_inst']).first()

    if institution:
        return jsonify({"Message": "Category already exist"})

    inst = Institution(
        name_inst=new_institution_data['name_inst'],
        info=new_institution_data['info'],
        count_student=new_institution_data['count_student'],
        city=new_institution_data['city'],
        military_department=new_institution_data['military_department'],
        category_acr_id=new_institution_data['category_acr_id'],
        user_id=new_institution_data['user_id']
    )
    print(new_institution_data['name_inst'])
    print(new_institution_data['name_inst'])
    db.session.add(inst)
    db.session.commit()
    return jsonify({"id": inst.id,
                    "name_inst": inst.name_inst,
                    "info": inst.info,
                    "count_student": inst.count_student,
                    "city": inst.city,
                    "military_department": inst.military_department,
                    "category_acr_id": inst.category_acr_id})


@api_teacher_blueprint.route('/institution/<int:id>', methods=['PUT', 'PATCH'])
@protected
def edit_institution(id):
    institution = Institution.query.get(id)
    if not institution:
        return jsonify({"Message": "Category does not exist"})

    update_category_data = request.get_json()
    institutions = Institution.query.filter_by(name_inst=update_category_data['name_inst']).first()
    if institutions:
        return jsonify({"Message": "Category already exist"})

    institution.name_inst = update_category_data['name_inst']
    institution.info = update_category_data['info']
    institution.count_student = update_category_data['count_student']
    institution.city = update_category_data['city']
    institution.military_department = update_category_data['military_department']
    institution.category_acr_id = update_category_data['category_acr_id']
    institution.user_id = update_category_data['user_id']

    db.session.add(institution)
    db.session.commit()

    return jsonify({"id": institution.id,
                    "name_inst": institution.name_inst,
                    "info": institution.info,
                    "count_student": institution.count_student,
                    "city": institution.city,
                    "military_department": institution.military_department,
                    "category_acr_id": institution.category_acr_id})


@api_teacher_blueprint.route('/institution/<int:id>', methods=['DELETE'])
@protected
def delete_institution(id):
    institution = Institution.query.get_or_404(id)
    db.session.delete(institution)
    db.session.commit()

    return jsonify({'Message': 'The category has been deleted!'})
