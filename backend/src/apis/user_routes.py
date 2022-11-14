from flask import Flask, jsonify, abort, request, Blueprint
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from models.user import User
from auth.auth import requires_auth
import logging
import datetime

user_app = Flask(__name__)
logging.basicConfig(filename='logs/{}.log'.format(datetime.date.today().strftime('%Y-%m-%d')), level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

user_app = Blueprint('user_app', __name__)
@user_app.route('/users')
def get_users():
    try:
        users = User.get_all_from_auth0()
        return jsonify({
            'success': True,
            'users': users
        })
    except Exception as e:
        user_app.logger.error(e)
        abort(500)

@user_app.route('/users/import')
def import_users():
    try:
        result = User.import_users()
        return jsonify({
            'success': True,
            'added': [u.format() for u in result[0]]
        })
    except Exception as e:
        user_app.logger.error(e)
        abort(500)