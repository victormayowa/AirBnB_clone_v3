#!/usr/bin/python3
'''API for a,menities.'''
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from flask import jsonify, request 
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


METHODS = ['GET', 'DELETE', 'POST', 'PUT']


@app_views.route('/amenities', methods=METHODS)
@app_views.route('/amenities/<amenity_id>', methods=METHODS)
def amenities(amenity_id=None):
    '''The amenity handler method'''
    hand = {
        'GET': get,
        'DELETE': remove,
        'POST': add,
        'PUT': update,
    }
    if request.method in hand:
        return hand[request.method](amenity_id)
    else:
        raise MethodNotAllowed(list(hand.keys()))


def get(amenity_id=None):
    '''retrieves all amenities.'''
    all_ame = storage.all(Amenity).values()
    if amenity_id:
        respond = list(filter(lambda x: x.id == amenity_id, all_amenities))
        if respond:
            return jsonify(respond[0].to_dict())
        raise NotFound()
    all_ame = list(map(lambda x: x.to_dict(), all_ame))
    return jsonify(all_ame)


def remove(amenity_id=None):
    '''Removes an amenity.'''
    all_ame = storage.all(Amenity).values()
    respond = list(filter(lambda x: x.id == amenity_id, all_ame))
    if respond:
        storage.delete(respond[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add(amenity_id=None):
    '''Adds new amenity'''
    d = request.get_json()
    if type(d) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in d:
        raise BadRequest(description='Missing name')
    new = Amenity(**d)
    new.save()
    return jsonify(new.to_dict()), 201


def update(amenity_id=None):
    '''Updates amenity'''
    keys = ('id', 'created_at', 'updated_at')
    all_ame = storage.all(Amenity).values()
    respond = list(filter(lambda x: x.id == amenity_id, all_ame))
    if respond:
        d = request.get_json()
        if type(d) is not dict:
            raise BadRequest(description='Not a JSON')
        old = respond[0]
        for k, v in d.items():
            if k not in keys:
                setattr(old, k, v)
        old.save()
        return jsonify(old.to_dict()), 200
    raise NotFound()
