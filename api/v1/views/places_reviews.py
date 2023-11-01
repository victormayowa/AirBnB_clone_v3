#!/usr/bin/python3
'''laces_reviews view for the API.'''
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def reviews_handler(place_id=None, review_id=None):
    '''handler for reviews'''
    h = {
        'GET': get_r,
        'DELETE': remove_r,
        'POST': add_r,
        'PUT': update_r
    }
    if request.method in h:
        return h[request.method](place_id, review_id)
    else:
        raise MethodNotAllowed(list(h.keys()))


def get_r(place_id=None, review_id=None):
    '''Gets the reviews'''
    if place_id:
        p = storage.get(Place, place_id)
        if p:
            rev = []
            for r in p.rev:
                rev.append(r.to_dict())
            return jsonify(rev)
    elif review_id:
        r = storage.get(Review, review_id)
        if r:
            return jsonify(r.to_dict())
    raise NotFound()


def remove_r(place_id=None, review_id=None):
    '''Removes review '''
    r = storage.get(Review, review_id)
    if r:
        storage.delete(r)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_r(place_id=None, review_id=None):
    '''Adds a new review'''
    p = storage.get(Place, place_id)
    if not p:
        raise NotFound()
    da = request.get_json()
    if type(d) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'user_id' not in d:
        raise BadRequest(description='Missing user_id')
    u = storage.get(User, data['user_id'])
    if not u:
        raise NotFound()
    if 'text' not in d:
        raise BadRequest(description='Missing text')
    d['place_id'] = place_id
    new = Review(**d)
    new.save()
    return jsonify(new.to_dict()), 201


def update_r(place_id=None, review_id=None):
    '''Update review'''
    keys = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    if review_id:
        r = storage.get(Review, review_id)
        if r:
            d = request.get_json()
            if type(d) is not dict:
                raise BadRequest(description='Not a JSON')
            for k, v in d.items():
                if k not in keys:
                    setattr(r, k, v)
            r.save()
            return jsonify(r.to_dict()), 200
    raise NotFound()
