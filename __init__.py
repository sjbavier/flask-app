from flask import Flask
from flask import request
app = Flask(__name__)

# POST /api/login
# POST /api/signup
# POST /api/token
# POST /api/logout
# GET /api/dashboard

@app.route('/api/login')
def login():
    """accepts user login credentials in request body"""
    """{ username, password }"""
    """generates access and refresh tokens"""

@app.route('/api/signup')
def signup():
    """accepts user sign up credentials in request body"""
    """checks for duplicates"""
    """{ username ,password }"""
    """hashes, salts and stores credentials in db"""

@app.route('/api/token')
def token():
    """after token expiration, checks refresh token"""
    """{ token }"""
    """generates new access token"""

@app.route('/api/logout')
def logout():
    """destroys tokens, sends client to login"""

@app.route('/api/dashboard')
def dashboard():
    """authenticated route"""