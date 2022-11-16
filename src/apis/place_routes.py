from flask import Flask, jsonify, abort, request, Blueprint
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from models.place import Place
from auth.auth import requires_auth
import datetime

place_app = Blueprint('place_app', __name__)

# This API returns all the palces
# This API does not need any permission and all the users can call it.
@place_app.route('/places')
def get_places():
    try:
        places = Place.get_all_formatted()
        return jsonify({
            'success': True,
            'places': places
        })
    except Exception as e:
        print(e)
        abort(500)

# This API returns a place by id. All the comments and likes are also returned. 
# This API does not need any permission and all the users can call it.
@place_app.route('/places/<int:place_id>')
def get_place_by_id(place_id):
    try:
        place = Place.get_by_id(place_id)
        return jsonify({
            'success': True,
            'place': place.format_with_comments()
        })
    except Exception as e:
        print(e)
        abort(500)

# This API posts a place 
# Member, admin and super admin users can call this API
@place_app.route('/places', methods=['POST'])
@requires_auth(permission='post:place')
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
        print(e)
        abort(500)

# This API patches a place
# Member, admin and super admin users can call this API
@place_app.route('/places/<int:place_id>', methods=['PATCH'])
@requires_auth(permission='patch:place')
def patch_place(user_id, place_id):
    
    try:
        place = Place.get_by_id(place_id)
        place.title=request.json.get('title')
        place.address=request.json.get('address')
        place.city=request.json.get('city')
        place.state=request.json.get('state')
        place.description=request.json.get('description')
        place.latitude=request.json.get('latitude')
        place.longitude=request.json.get('longitude')

        place.update()
        return jsonify({
            'success': True,
            'place': place.format()
        })
    except Exception as e:
        print(e)
        abort(500)

# This API deletes a place
# Only admin and super admin users can delete places (Member users only can delete places that are added by themselfs)
@place_app.route('/places/<int:place_id>', methods=['DELETE'])
@requires_auth('delete:place')
def delete_place(user_id, place_id):
    try:
        place = Place.get_by_id(place_id)
        # if place.user_id != user_id:
        #     abort(403)
        if place is None:
            abort(404)
        else:
            place.delete()
        return jsonify({
            'success': True,
            'place': place.format()
        })
    except Exception as e:
        print(e)
        abort(500)

# This API deletes a list of places
# Only super admin can call this API
@place_app.route('/delete_place_bulk', methods=['POST'])
@requires_auth('bulkdelete:place')
def delete_places_bulk(user_id):
    try:
        ids = request.json.get('ids')
        result = Place.delete_bulk(ids)
        return jsonify({
            'deleted': result[0],
            'error_occured': result[1]
        })
    except Exception as e:
        print(e)
        abort(500)