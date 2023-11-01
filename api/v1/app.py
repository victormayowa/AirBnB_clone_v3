#!/usr/bin/python3
""" the api flask app"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors and return a JSON response."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def bad_request(e):
    '''Handles the 400 HTTP error code and return JSON RESPONSE.'''
    m = 'Bad request'
    if isinstance(e, Exception) and hasattr(e, 'description'):
        m = e.description
    return jsonify(e=m), 400


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
