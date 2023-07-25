#!/usr/bin/python3
""" View for places """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place_city(city_id):
    """ Gets a place with the city id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in storage.all(Place).values()
              if place.city_id == city_id]
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Gets a place with the place id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place with the place id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a place linked to a city by the id and json data"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    js_data = request.get_json()
    if 'user_id' not in js_data:
        abort(400, 'Missing user_id')
    if 'name' not in js_data:
        abort(400, 'Missing name')
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    user = storage.get(User, js_data['user_id'])
    if user is None:
        abort(404)
    place = Place(**js_data)
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Updates a place based on the place id and json data"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.is_json is False:
        abort(400, 'Not a JSON')
    js_data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, val in js_data.items():
        if key not in ignore_keys:
            setattr(place, key, val)
    place.save()
    return jsonify(place.to_dict()), 200
