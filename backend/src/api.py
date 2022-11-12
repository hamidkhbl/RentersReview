import datetime
from flask import Flask, jsonify, abort, request
from .models.place import Place
from .models.comment import Comment
from .models.like import Like
from .models.base import setup_db
from .models.user import User
from .auth.auth import requires_auth
import logging

app = Flask(__name__)
setup_db(app)
print(str(datetime.date.today))
logging.basicConfig(filename='logs/{}.log'.format(datetime.date.today().strftime('%Y-%m-%d')), level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/')
def index():
    return "not implemented"

# Returns users from Auth0
# Needs the super admin previlage

# region user


@app.route('/users')
def get_users():
    try:
        users = User.get_all_from_auth0()
        return jsonify({
            'success': True,
            'users': users
        })
    except Exception as e:
        app.logger.error(e)
        abort(500)

@app.route('/users/import')
def import_users():
    try:
        result = User.import_users()
        return jsonify({
            'success': True,
            'added': [u.format() for u in result[0]]
        })
    except Exception as e:
        app.logger.error(e)
        abort(500)

# endregion

# region place

@app.route('/places')
def get_places():
    try:
        places = Place.get_all_formatted()
        return jsonify({
            'success': True,
            'places': places
        })
    except Exception as e:
        app.logger.error(e)
        abort(500)
    
@app.route('/places', methods=['POST'])
@requires_auth(permission='read:place')
def add_place(user_id):
    try:
        place = Place(
            title=request.json.get('title'),
            address=request.json.get('address'),
            city=request.json.get('city'),
            state=request.json.get('state'),
            description=request.json.get('description'),
            latitude=request.json.get('latitude'),
            longitude=request.json.get('longitude'),
            user_id=user_id
        )

        place.insert()
        return jsonify({
            'success': True,
            'place': place.format()
        })
    except Exception as e:
        app.logger.error(e)
        abort(500)

@app.route('/places/<int:place_id>', methods=['DELETE'])
@requires_auth('read:place')
def delete_place(user_id, place_id):
    try:
        place = Place.get_by_id(place_id)
        if place.user_id != user_id:
            abort(403)
        if place is None:
            abort(404)
        else:
            place.delete()
        return jsonify({
            'success': True,
            'place': place.format()
        })
    except Exception as e:
        app.logger.error(e)
        abort(500)


@app.route('/delete_place_bulk', methods=['POST'])
def delete_places_bulk():
    try:
        ids = request.json.get('ids')
        result = Place.delete_bulk(ids)
        return jsonify({
            'deleted': result[0],
            'error_occured': result[1]
        })
    except Exception as e:
        app.logger.error(e)
        abort(500)

@app.route('/places/<int:place_id>')
def get_place_by_id(place_id):
    try:
        place = Place.get_by_id(place_id)
        return jsonify({
            'success': True,
            'place': place.format_with_comments()
        })
    except Exception as e:
        app.logger.error(e)
        abort(500)
# endregion

# region comment


@app.route('/places/<int:place_id>/comments')
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

@app.route('/comments', methods=['POST'])
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
        app.logger.error(e)
        abort(500)

# endregion

# region like

@app.route('/like', methods=['POST'])
@requires_auth('read:place')
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
        app.logger.error(e)
        abort(500)
        
# endregion
