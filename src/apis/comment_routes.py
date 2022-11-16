from flask import Flask, jsonify, abort, request, Blueprint
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from models.comment import Comment
from auth.auth import requires_auth

import datetime

comment_app = Flask(__name__)
comment_app = Blueprint('comment_app', __name__)

@comment_app.route('/places/<int:place_id>/comments')
def place_cooments(place_id):
    try:
        comments = Comment.get_place_comments_formatted(place_id)
        return jsonify({
            'success': True,
            'comments': comments
        })
    except Exception as e:
        print(e)
        abort(500)

@comment_app.route('/comments', methods=['POST'])
@requires_auth(permission='post:comment')
def add_comment_for_place(user_id):
    try:
        comment = Comment(
            title=request.json.get('title'),
            creation_date=str(datetime.datetime.now()),
            description=request.json.get('title'),
            place_id=request.json.get('place_id'),
            user_id=user_id
        )
        comment.insert()
        return jsonify({
            'success': True,
            'comment': comment.format()
        })
    except Exception as e:
        print(e)
        abort(500)
        
@comment_app.route('/comment/<int:comment_id>', methods=['DELETE'])
@requires_auth('delete:comment')
def delete_place(user_id, comment_id):
    try:
        comment = Comment.get_by_id(comment_id)
        # if comment.user_id != user_id:
        #     abort(403)
        if comment is None:
            abort(404)
        else:
            comment.delete()
        return jsonify({
            'success': True,
            'place': comment.format()
        })
    except Exception as e:
        print(e)
        abort(500)