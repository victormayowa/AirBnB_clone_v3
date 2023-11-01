#!/usr/bin/python3
'''tes view for the API.'''
from models import storage
from models.state import State
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from api.v1.views import app_views


METHODS = ['GET', 'DELETE', 'POST', 'PUT']


@app_views.route('/states', methods=METHODS)
@app_views.route('/states/<state_id>', methods=METHODS)
def states_handler(state_id=None):
    '''handles states endpoint'''
    h = {
        'GET': get_s,
        'DELETE': remove_s,
        'POST': add_s,
        'PUT': update_s,
    }
    if request.method in h:
        return h[request.method](state_id)
    else:
        raise MethodNotAllowed(list(h.keys()))


def get_s(state_id=None):
    '''Gets all state'''
    all_s = storage.all(State).values()
    if state_id:
        r = list(filter(lambda x: x.id == state_id, all_s))
        if r:
            return jsonify(r[0].to_dict())
        raise NotFound()
    all_s = list(map(lambda x: x.to_dict(), all_s))
    return jsonify(all_s)


def remove_s(state_id=None):
    '''deletes a state'''
    all_s = storage.all(State).values()
    r = list(filter(lambda x: x.id == state_id, all_s))
    if r:
        storage.delete(r[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_s(state_id=None):
    '''puts a new state'''
    d = request.get_json()
    if type(d) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in d:
        raise BadRequest(description='Missing name')
    new = State(**d)
    new.save()
    return jsonify(new.to_dict()), 201


def update_s(state_id=None):
    '''Updates the state'''
    keys = ('id', 'created_at', 'updated_at')
    all_s = storage.all(State).values()
    r = list(filter(lambda x: x.id == state_id, all_s))
    if r:
        d = request.get_json()
        if type(d) is not dict:
            raise BadRequest(description='Not a JSON')
        old = r[0]
        for k, v in d.items():
            if k not in keys:
                setattr(old, k, v)
        old.save()
        return jsonify(old.to_dict()), 200
    raise NotFound()
