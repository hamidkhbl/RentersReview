import os, sys
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from src.apis.like_routes import like_app
from src.apis.comment_routes import comment_app
from src.apis.user_routes import user_app
from src.apis.place_routes import place_app
from models.base import setup_db
import datetime
from flask import Flask, jsonify
import sys
import os
from flask import render_template

app = Flask(__name__)
setup_db(app)


app.register_blueprint(user_app)
app.register_blueprint(place_app)
app.register_blueprint(comment_app)
app.register_blueprint(like_app)


@app.route('/')
def method_name():
    return render_template("login.html")

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found."
    }), 404
    
@app.errorhandler(401)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401
    
@app.errorhandler(403)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "You don't have the permission to access the requested resource."
    }), 403

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
