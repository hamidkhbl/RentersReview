from flask import Flask, jsonify, abort, request, Blueprint
from ..models.place import Place
from ..auth.auth import requires_auth
import logging
import datetime

place_app = Flask(__name__)
logging.basicConfig(filename='logs/{}.log'.format(datetime.date.today().strftime('%Y-%m-%d')), level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

place_app = Blueprint('place_app', __name__)
@place_app.route('/places')
def get_places():
    try:
        places = Place.get_all_formatted()
        return jsonify({
            'success': True,
            'places': places
        })
    except Exception as e:
        place_app.logger.error(e)
        abort(500)

@place_app.route('/places', methods=['POST'])
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
        place_app.logger.error(e)
        abort(500)
        
@place_app.route('/places/<int:place_id>', methods=['DELETE'])
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
        place_app.logger.error(e)
        abort(500)

@place_app.route('/delete_place_bulk', methods=['POST'])
def delete_places_bulk():
    try:
        ids = request.json.get('ids')
        result = Place.delete_bulk(ids)
        return jsonify({
            'deleted': result[0],
            'error_occured': result[1]
        })
    except Exception as e:
        place_app.logger.error(e)
        abort(500)

@place_app.route('/places/<int:place_id>')
def get_place_by_id(place_id):
    try:
        place = Place.get_by_id(place_id)
        return jsonify({
            'success': True,
            'place': place.format_with_comments()
        })
    except Exception as e:
        place_app.logger.error(e)
        abort(500)