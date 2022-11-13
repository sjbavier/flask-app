from app import jwt_required
from app.auth.decorators import permission_required
from app.models.user import Permission
from . import api
from ..models.reference import ReferenceStructure, ReferenceSchema, ReferenceStructureSchema

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

# @api.route('/reference/path/<path_name>', methods=['GET'])
# @jwt_required()
# @permission_required(Permission.READ)
# def get_reference_path():
