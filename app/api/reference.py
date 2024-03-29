from flask import request, jsonify

from app import jwt_required
from app.auth.decorators import permission_required
from app.models.user import Permission
from . import api
from ..models.reference import ReferenceStructure, ReferenceSchema, ReferenceStructureSchema, Reference

reference_structure_schema = ReferenceStructureSchema()
reference_schema = ReferenceSchema()


# ///////////////////
# Reset Reference
# ///////////////////

@api.route('/reference/build', methods=['POST'])
# @jwt_required()
# @permission_required(Permission.WRITE)
def build_reference():
    print('todo')


# ///////////////////
# Reset Reference
# ///////////////////

# @api.route('/reference/path/<str:path>', methods=['GET'])
# @jwt_required()
# @permission_required(Permission.EXECUTE)
# def get_reference(path: int):
#

# ///////////////////
# GET Reference Structure
# ///////////////////

@api.route('/reference/structure', methods=['GET'])
@jwt_required()
@permission_required(Permission.READ)
def get_reference_structure():
    structure = ReferenceStructure.query.order_by(ReferenceStructure.reference_structure_id.desc()).first()
    return reference_structure_schema.dump(structure)


@api.route('/reference/path', methods=['GET'])
@jwt_required()
@permission_required(Permission.READ)
def get_reference_path():
    path_name = request.args.get("name")
    reference = Reference.query.filter_by(path=path_name).first()
    if reference:
        return jsonify(data=reference_schema.dump(reference))
    else:
        return jsonify(message=f'No file found at path {path_name}'), 404
