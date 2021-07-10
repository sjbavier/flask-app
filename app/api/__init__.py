from flask import Blueprint

"""
The Blueprint class constructor takes a name
and location of the package or module
"""
api = Blueprint('api', __name__)

from . import views, errors
