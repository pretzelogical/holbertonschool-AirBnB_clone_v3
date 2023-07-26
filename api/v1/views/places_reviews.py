#!/usr/bin/python3
""" View for place reviews """
from flask import jsonify, abort, request, make_response
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
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.is_json is False:
        abort(400, 'Not a JSON')
    new_review = request.get_json(silent=True)
    if "text" not in new_review.keys():
        abort(400, "Missing text")
    if "user_id" not in new_review.keys():
        abort(400, "Missing user id")
    user = storage.get(User, new_review['user_id'])
    if user is None:
        abort(404)
    new_obj = Review(text=new_review['text'],
                     user_id=new_review['user_id'],
                     place_id=place_id)
    storage.new(new_obj)
    storage.save()
    return new_obj.to_dict(), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a reviews from the review_id & json data"""
    if request.is_json is False:
        abort(400, "Not a JSON")
    new = request.get_json(silent=True)
    old = storage.get(Review, review_id)
    if not old:
        abort(404)
    for key, value in new.items():
        if key not in ['id',
                       'created_at',
                       'updated_at',
                       'user_id',
                       'place_id']:
            setattr(old, key, value)
    storage.save()
    return jsonify(old.to_dict()), 200
