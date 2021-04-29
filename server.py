#!/usr/bin/env python
"""
Main server file for flask
"""
# coding: utf-8

import flask
import flask_restful

import service


# Create a "Flask-Restful" Application
APP = flask.Flask(__name__)
API = flask_restful.Api(app=APP)


@APP.errorhandler(404)
def resource_not_found(error):
    """Do not let Flask handle generic 404 errors natively.
    It will return HTML even though the client accept header will specify JSON.
    :param error: The exception
    :returns: JSON 404 response
    """
    print('Not Found: {}'.format(error))
    msg = 'Resource Not Found'
    desc = 'The requested URL was not found on the server.'
    return service.util.make_response_object({'message': msg, 'description': desc}, response_code=404)


# resource paths
API.add_resource(service.reviews.ReviewRequestHandler, '/api/reviews')


if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=8019, debug=True)
