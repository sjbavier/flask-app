from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.models.user import User
from app.models.role import Role


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://cra_user:xyz-replace-with-secret@localhost:3306/webmane'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
'''
add flask-migrate alembic wrapper, necessary for 'flask db init' and 'flask db migrate'
'''
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

# POST /api/login
# POST /api/signup
# POST /api/token
# POST /api/logout
# GET /api/dashboard

@app.route('/api/login')
def login():
    """
    accepts user login credentials in request body
    { username, password }
    generates access and refresh tokens
    """

@app.route('/api/signup')
def signup():
    """
    accepts user sign up credentials in request body
    checks for duplicates
    { username ,password }
    hashes, salts and stores credentials in db
    """

@app.route('/api/token')
def token():
    """
    after token expiration, checks refresh token
    { token }
    generates new access token
    """

@app.route('/api/logout')
def logout():
    """
    destroys tokens, sends client to login
    """

@app.route('/api/dashboard')
def dashboard():
    """
    authenticated route
    """