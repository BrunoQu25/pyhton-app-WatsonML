from flask import Blueprint, jsonify
# from flask_cors import cross_origin

from services import watson

from exceptions.unauthorized import Unauthorized
from exceptions.watson_error import WatsonError

watson_routes = Blueprint('watson_routes', __name__)

@watson_routes.route('/classify', methods=['POST'])
# @cross_origin()
def watson_classify():
    return watson.classify()

@watson_routes.errorhandler(Unauthorized)
def handle_unauthorized(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@watson_routes.errorhandler(WatsonError)
def handle_watsonerror(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response