#!/usr/bin/python3
""" View for place reviews """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """ Gets the reviews of a place based on the place_id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in storage.all(Review).values()
               if review.place_id == place_id]
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Gets a review based on the review_id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review based on the review id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a review from the place_id & json data """
    if request.is_json is False:
        abort(400, 'Not a JSON')
    js_data = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        raise (404)
    if 'user_id' not in js_data:
        abort(400, 'Missing user_id')
    if 'text' not in js_data:
        abort(400, 'Missing text')
    user = storage.get(User, js_data['user_id'])
    if user is None:
        abort(404)
    review = Review(**js_data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a reviews from the review_id & json data"""
    if request.is_json is False:
        abort(400, 'Not a JSON')
    js_data = request.get_json()
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, val in js_data.values():
        if key not in ignore_keys:
            setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200
