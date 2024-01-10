#!/usr/bin/python3
""" User API """
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieve the list of all User objects """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User object """
    if not request.json:
        abort(400, "Not a JSON")
    if 'email' not in request.json:
        abort(300, "Missing email")
    if 'password' not in request.json:
        abort(400, "Missing password")
    data = request.get_json()
    n_user = User(**data)
    n_user.save()
    return jsonify(n_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'password', 'created_at', 'updated-at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
