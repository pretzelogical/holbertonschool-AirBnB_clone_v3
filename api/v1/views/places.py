#!/usr/bin/python3
""" View for places """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models import storage


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place(city_id):
    """ Gets a place with the city id """
    places = storage.get(City, city_id).places
    if places is None:
        abort(404)
    return jsonify(places)
