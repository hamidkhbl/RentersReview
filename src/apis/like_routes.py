from flask import Flask, jsonify, abort, request, Blueprint
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from models.like import Like
from auth.auth import requires_auth
import logging
import datetime

like_app = Flask(__name__)
logging.basicConfig(filename='logs/{}.log'.format(datetime.date.today().strftime('%Y-%m-%d')), level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

like_app = Blueprint('like_app', __name__)

@like_app.route('/like', methods=['POST'])
@requires_auth('post:like')
def like(user_id):
    try:
        comment_id=request.json.get('comment_id')
        like = Like(
            comment_id=comment_id,
            user_id=user_id
            )
        result = like.like()
        return jsonify({
                'success': True,
                'like': result
            })
    except Exception as e:
        like_print(e)
        abort(500)