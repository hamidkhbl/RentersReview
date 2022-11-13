from flask import Flask, jsonify, abort, request, Blueprint
from ..models.comment import Comment
from ..auth.auth import requires_auth
import logging
import datetime

comment_app = Flask(__name__)
logging.basicConfig(filename='logs/{}.log'.format(datetime.date.today().strftime('%Y-%m-%d')), level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

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
        app.logger.error(e)
        abort(500)

@comment_app.route('/comments', methods=['POST'])
@requires_auth(permission='read:place')
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
        comment_app.logger.error(e)
        abort(500)