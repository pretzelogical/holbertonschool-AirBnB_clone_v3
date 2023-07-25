#!/usr/bin/python3
""" Create a new view for states and handle RESTFul API """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """ Retrives City objects of a State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    cities_s = [city.to_dict() for city in cities]
    return jsonify(cities_s)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_cities_id(city_id):
    """ Retrives City objects when an id is provided """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Delete a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city_post(state_id):
    """ Creates a city """
    if request.is_json is False:
        abort(400, 'Not a JSON')
    js_data = request.get_json()
    if 'name' not in js_data:
        abort(400, 'Missing name')
    c_state = storage.get(State, state_id)
    if c_state is None:
        abort(404)
    city = City(**js_data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.is_json is False:
        abort(400, 'Not a JSON')
    data = request.get_json()
    # Ignore keys: id, created_at, and updated_at
    ignored_keys = ['id', 'created_at', 'updated_at', 'state_id']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
