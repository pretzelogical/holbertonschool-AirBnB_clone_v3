#!/usr/bin/python3
""" View for place reviews """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models import storage


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in storage.all(Review).values()
               if review.place_id == place_id]
    return jsonify(reviews)

