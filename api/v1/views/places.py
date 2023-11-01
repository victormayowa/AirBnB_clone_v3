#!/usr/bin/python3
'''places view API.'''
from models import storage, storage_t
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from api.v1.views import app_views
from models import storage, storage_t


@app_views.route('/cities/<city_id>/places/', methods=['GET'],
                 strict_slashes=False)
def get_cty_places(city_id):
    c = storage.get(City, city_id)
    if not c:
        abort(404)
    city_p = [p.to_dict() for p in storage.all(Place).values()
                   if p.city_id == city_id]
    return jsonify(city_p)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_p(place_id):
    ''' get place'''
    p = storage.get(Place, place_id)
    if not p:
        abort(404)
    return jsonify(p.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_p(place_id):
    p = storage.get(Place, place_id)
    if not p:
        abort(404)
    storage.delete(p)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places/', methods=['POST'],
                 strict_slashes=False)
def create_p(city_id):
    ''' create a place'''
    c = storage.get(City, city_id)
    if not c:
        abort(404)
    d = request.get_json(silent=True)
    if not d:
        return make_response('Not a JSON', 400)
    if 'user_id' not in d:
        return make_response('Missing user_id', 400)
    u = storage.get(User, d['user_id'])
    if not u:
        abort(404)
    if 'name' not in d:
        return make_response('Missing name', 400)
    p = Place(city_id=city_id, user_id=user.id, name=d['name'])
    p.save()
    return make_response(jsonify(p.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_p(place_id):
    ''' update place'''
    p = storage.get(Place, place_id)
    if not p:
        abort(404)
    d = request.get_json(silent=True)
    if not d:
        return make_response('Not a JSON', 400)
    for key, val in d.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(p, key, val)
    p.save()
    return make_response(jsonify(p.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'])
def search_place():
    ''' search a place'''
    d = request.get_json(silent=True)
    if type(d) is not dict:
        return make_response('Not a JSON', 400)

    all_p = storage.all(Place)
    m = set()
    states = d.get('states') if d.get('states') else []
    cities = d.get('cities') if d.get('cities') else []
    amenities = d.get('amenities') if d.get('amenities') else []
    empty = not states and not cities and not amenities
    if empty:
        m = set(all_p.values())

    for state_id in states:
        state = storage.get(State, state_id)
        places_in_state = {p for p in all_p.values()
                           if storage.get(City, p.city_id) in state.cities}
        m = m.union(places_in_state)
    for city_id in cities:
        places_in_city = {p for p in all_p.values()
                          if p.city_id == city_id}
        m = m.union(places_in_city)

    if amenities:
        if len(m) == 0:
            m = set(all_p.values())
        amenities = {storage.get(Amenity, amenity_id)
                     for amenity_id in amenities}
        m = {p for p in m
                 if amenities.intersection(set(p.amenities)) == amenities}

    final_m = []
    for p in m:
        place_d = p.to_dict()
        place_d.pop('amenities', None)
        final_m.append(place_d)

    return jsonify(final_m)
