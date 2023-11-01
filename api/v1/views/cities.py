#!/usr/bin/python3
'''API for cities.'''
from models import storage, storage_t
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from flask import jsonify, request


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def cities_handler(state_id=None, city_id=None):
    '''handles cities endpoint.'''
    h = {
        'GET': get_c,
        'DELETE': remove_c,
        'POST': add_c,
        'PUT': update_c,
    }
    if request.method in h:
        return h[request.method](state_id, city_id)
    else:
        raise MethodNotAllowed(list(h.keys()))


def get_c(state_id=None, city_id=None):
    '''Gets the city'''
    if state_id:
        s = storage.get(State, state_id)
        if s:
            c = list(map(lambda x: x.to_dict(), s.cities))
            return jsonify(c)
    elif city_id:
        ci = storage.get(City, city_id)
        if ci:
            return jsonify(ci.to_dict())
    raise NotFound()


def remove_c(state_id=None, city_id=None):
    '''Removes a city'''
    if city_id:
        cty = storage.get(City, city_id)
        if cty:
            storage.delete(cty)
            if storage_t != "db":
                for p in storage.all(Place).values():
                    if p.city_id == city_id:
                        for r in storage.all(Review).values():
                            if r.place_id == place.id:
                                storage.delete(r)
                        storage.delete(p)
            storage.save()
            return jsonify({}), 200
    raise NotFound()


def add_c(state_id=None, city_id=None):
    '''Adds new city.'''
    s = storage.get(State, state_id)
    if not s:
        raise NotFound()
    d = request.get_json()
    if type(d) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in d:
        raise BadRequest(description='Missing name')
    d['state_id'] = state_id
    city = City(**d)
    city.save()
    return jsonify(city.to_dict()), 201


def update_c(state_id=None, city_id=None):
    '''Updates city'''
    keys = ('id', 'state_id', 'created_at', 'updated_at')
    if city_id:
        c = storage.get(City, city_id)
        if c:
            d = request.get_json()
            if type(d) is not dict:
                raise BadRequest(description='Not a JSON')
            for k, v in d.items():
                if k not in keys:
                    setattr(c, k, v)
            c.save()
            return jsonify(c.to_dict()), 200
    raise NotFound()
