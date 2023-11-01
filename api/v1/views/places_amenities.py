#!/usr/bin/python3
""" handles place_amenity objects api"""
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place
from flask import jsonify, abort, make_response
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities/', methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id):
    p = storage.get(Place, place_id)
    if not p:
        abort(404)
    place_amenities = []
    for a in place.amenities:
        place_amenities.append(a.to_dict())
    return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_a(place_id, amenity_id):
    p = storage.get(Place, place_id)
    if not p:
        abort(404)
    a = storage.get(Amenity, amenity_id)
    if not a:
        abort(404)
    if storage_t == 'db':
        abort(404) if a not in p.amenities\
         else p.amenities.remove(a)
    else:
        abort(404) if a.id not in p.amenity_ids\
         else p.amenity_ids.remove(a.id)
    p.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_a(place_id, amenity_id):
    p = storage.get(Place, place_id)
    if not p:
        abort(404)
    a = storage.get(Amenity, amenity_id)
    if not a:
        abort(404)
    if a in p.amenities:
        return make_response(jsonify(a.to_dict()), 200)
    if storage_t == 'db':
        p.amenities.append(a)
    else:
        p.amenity_ids.append(a.id)
    p.save()
    return make_response(jsonify(a.to_dict()), 201)
