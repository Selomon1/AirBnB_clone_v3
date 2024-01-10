#!/usr/bin/python3
""" Place Api object """
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """ Retrieves all place objects of a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create place(city_id):
    """ Create a new Place in a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data or not isinstance(data, dict):
        abort(400, "Not a JSON")

    required_keys = ['user_id', 'name']
    missing_keys = [key for key in required_keys if not in data]
    if missing_keys:
        abort(400, f"Missing keys: {', '.join(missing_key)}")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['city_id'] = city_id
    n_place = Place(**data)
    n_place.save()
    return jsonify(n_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Update a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data or not isinstance(data, dict):
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
