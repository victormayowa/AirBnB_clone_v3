#!/usr/bin/python3
'''sers view for the API.'''
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def get_u(user_id=None):
    '''Gets the user'''
    if user_id:
        u = storage.get(User, user_id)
        if u:
            o = u.to_dict()
            if 'places' in o:
                del o['places']
            if 'reviews' in o:
                del o['reviews']
            return jsonify(o)
        raise NotFound()
    all_u = storage.all(User).values()
    users = []
    for u in all_u:
        o = u.to_dict()
        if 'places' in o:
            del o['places']
        if 'reviews' in o:
            del o['reviews']
        users.append(o)
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def remove_u(user_id):
    '''Removes'''
    u = storage.get(User, user_id)
    if u:
        storage.delete(u)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route('/users', methods=['POST'])
def add_u():
    '''Adds'''
    d = {}
    try:
        d = request.get_json()
    except Exception:
        d = None
    if type(d) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'email' not in d:
        raise BadRequest(description='Missing email')
    if 'password' not in d:
        raise BadRequest(description='Missing password')
    u = User(**d)
    u.save()
    o = u.to_dict()
    if 'places' in o:
        del o['places']
    if 'reviews' in o:
        del o['reviews']
    return jsonify(o), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_u(user_id):
    '''Update'''
    keys = ('id', 'email', 'created_at', 'updated_at')
    u = storage.get(User, user_id)
    if u:
        d = {}
        try:
            d = request.get_json()
        except Exception:
            d = None
        if type(d) is not dict:
            raise BadRequest(description='Not a JSON')
        for k, v in d.items():
            if k not in keys:
                setattr(u, k, v)
        u.save()
        o = u.to_dict()
        if 'places' in o:
            del o['places']
        if 'reviews' in o:
            del o['reviews']
        return jsonify(o), 200
    raise NotFound()
