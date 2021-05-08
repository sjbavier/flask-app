from flask import Blueprint

"""
The Blueprint class constructor takes a name
and location of the package or module
"""
main = Blueprint('main', __name__)

from . import views, errors
