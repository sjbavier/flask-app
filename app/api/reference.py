import os
from .. import db
from . import api
from flask import jsonify
from app import jwt_required, request, config
from app.auth.decorators import permission_required, debug
from app.models.user import Permission


# ///////////////////
# Reset Reference
# ///////////////////

@api.route('/reference/build', methods=['POST'])
# @jwt_required()
# @permission_required(Permission.WRITE)
def build_reference():
    print('todo')

