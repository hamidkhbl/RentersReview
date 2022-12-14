from flask import Flask, jsonify, abort, request, Blueprint
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from models.user import User
from auth.auth import requires_auth
import datetime
user_app = Flask(__name__)

user_app = Blueprint('user_app', __name__)
@user_app.route('/users')
@requires_auth(permission='get:user')
def get_users(user_id):
    try:
        users = User.get_all_from_auth0()
        return jsonify({
            'success': True,
            'users': users
        })
    except Exception as e:
        print(e)
        abort(500)

@user_app.route('/users/import')
@requires_auth(permission='get:user')
def import_users(user_id):
    try:
        result = User.import_users()
        return jsonify({
            'success': True,
            'added': [u.format() for u in result[0]]
        })
    except Exception as e:
        print(e)
        abort(500)