#!/usr/bin/python3
# api/v1/views/index.py
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
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    
    stats = {cls: storage.count(c) for c, cls in classes.items()}
    # Convert the dictionary to a formatted JSON string
    json_stats = json.dumps(stats, indent=2)
    # Add new lines between each key-value pair
    formatted_stats = "\n".join(json_stats.splitlines())
    
    return formatted_stats, 200, {'Content-Type': 'application/json'}
