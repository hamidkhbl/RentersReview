import logging
from apis.like_routes import like_app
from apis.comment_routes import comment_app
from apis.user_routes import user_app
from apis.place_routes import place_app
from models.base import setup_db
import datetime
from flask import Flask, jsonify
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

app = Flask(__name__)
setup_db(app)
logging.basicConfig(filename='logs/{}.log'.format(datetime.date.today().strftime('%Y-%m-%d')),
                    level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.register_blueprint(user_app)
app.register_blueprint(place_app)
app.register_blueprint(comment_app)
app.register_blueprint(like_app)


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found."
    }), 404

@app.errorhandler(405)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed."
    }), 405

@app.errorhandler(422)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Request cannot be processed."
    }), 422

@app.errorhandler(409)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 409,
        "message": "Resource already exists."
    }), 409

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Something went wrong!"
    }), 500
