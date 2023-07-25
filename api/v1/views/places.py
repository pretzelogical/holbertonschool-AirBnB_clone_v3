#!/usr/bin/python3
""" View for places """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models import storage


@app_views.route('/places', methods=['GET'],
                 strict_slashes=False)
def get_place_no_id():
    """ Gets an place if no id has been provided """
    places = storage.all(Place).values()
    return jsonify([p.to_dict() for p in places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id=None):
    """ Gets an place when an id is provided """
    places = storage.all(Place)
    p_key = "Place." + place_id
    if p_key not in places:
        abort(404)
    return (jsonify(places[p_key].to_dict()))


@app_views.route('/places', methods=['POST'],
                 strict_slashes=False)
def new_place():
    """ Creates a new place """
    js_info = request.get_json()
    if request.is_json is False:
        abort(400, 'Not a JSON')
    if 'email' not in js_info:
        abort(400, 'Missing email')
    if 'password' not in js_info:
        abort(400, 'Missing password')
    new_p = Place(**js_info)
    new_p.save()
    return jsonify(new_p.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """ Deletes an place based on the place id """
    places = storage.all(Place)
    p_key = "Place." + place_id
    if p_key not in places:
        abort(404)
    storage.delete(places[p_key])
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id=None):
    """ Updates an place based on the place id """
    js_info = request.get_json()
    places = storage.all(Place)
    if request.is_json is False:
        abort(400, 'Not a JSON')
    js_info.pop('id', 'no_error_pls')
    js_info.pop('created_at', 'no_error_pls')
    js_info.pop('updated_at', 'no_error_pls')
    js_info.pop('email', 'no_error_pls')
    c_key = "Place." + place_id
    if c_key not in places:
        abort(404)
    for key, val in js_info.items():
        setattr(places[c_key], key, val)
    storage.save()
    return jsonify(places[c_key].to_dict()), 200
