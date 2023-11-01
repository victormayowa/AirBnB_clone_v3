#!/usr/bin/python3
''' the index for app_view'''
import json
from flask import jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """Returns the status of your API."""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Retrieves the number of each object type."""
    obj = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for k, v in obj.items():
        obj[k] = storage.count(v)
    return jsonify(obj)
