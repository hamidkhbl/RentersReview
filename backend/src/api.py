from flask import Flask, jsonify, abort

from .models.base import setup_db
from .models.user import User

app = Flask(__name__)
setup_db(app)

@app.route('/')
def method_name():
    return "not implemented"

# Returns users from Auth0
# Needs the super admin previlage
@app.route('/users')
def get_users():
    try:
        users = User.get_all_from_auth0()
        return jsonify({
            'success': True,
            'users': users
        })
    except:
        abort(500)