from flask import Flask, jsonify, abort, request
from .models.place import Place

from .models.base import setup_db
from .models.user import User

app = Flask(__name__)
setup_db(app)

@app.route('/')
def index():
    return "not implemented"

# Returns users from Auth0
# Needs the super admin previlage
@app.route('/users')
def get_users():
    try:
        users = User.get_all_from_auth0()
        return jsonify({
            'success': True,
            'users': users
        })
    except:
        abort(500)
        
@app.route('/places')
def get_places():
    places = Place.get_all_formatted()
    return jsonify({
        'success': True,
        'places': places
    })
    
@app.route('/places', methods=['POST'])
def add_place():
    place = Place(
        title = request.json.get('title'),
        address = request.json.get('address'),
        city = request.json.get('city'),
        state = request.json.get('state'),
        description = request.json.get('description'),
        latitude = request.json.get('latitude'),
        longitude = request.json.get('longitude')
    )
    
    place.insert()
    return jsonify({
        'success': True,
        'place': place.format()
    })
    
@app.route('/places/<int:place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = Place.get_by_id(place_id)
    if place is None:
        abort(404)
    else:
        place.delete()
    return jsonify({
        'success': True,
        'place': place.format()
    })

@app.route('/delete_place_bulk', methods=['POST'])
def delete_places_bulk():
    ids = request.json.get('ids')
    result = Place.delete_bulk(ids)
    return jsonify({
        'deleted':result[0],
        'error_occured': result[1]
    })