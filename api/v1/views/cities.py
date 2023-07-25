#!/usr/bin/python3
""" Create a new view for states and handle RESTFul API """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', method=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """ Retrives City objects of a State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ gits the states """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """ gits the states """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict()), 200


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


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_post():
    if request.is_json is False:
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    if request.is_json is False:
        abort(400, 'Not a JSON')
    data = request.get_json()
    states = storage.all(State)
    s_key = "State." + state_id
    if s_key not in states:
        abort(404)
    # Ignore keys: id, created_at, and updated_at
    ignored_keys = ['id', 'created_at', 'updated_at', 'state_id']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(states[s_key], key, value)
    storage.save()
    return jsonify(states[s_key].to_dict()), 200
