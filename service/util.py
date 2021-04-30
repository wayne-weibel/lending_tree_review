"""
utility function
"""
import json
import flask

# Generic Constants
BASE_REVIEW_URL = 'https://www.lendingtree.com/reviews'

CONTENT_TYPE_TEXT = 'text/plain'
CONTENT_TYPE_JSON = 'application/json; charset=utf-8'

STARS_RGX = r'\((\d+)\s+of\s+(\d+)\).*'
DATE_PARSE = 'Reviewed in %B %Y'

def make_response_object(body, headers=None, response_code=200):
    """Format response according to accept header.
    Build a Response() object from body/response code. Set any headers appropriately.

    :param headers: Dictionary of HTTP headers to return.
    :param response_code: HTTP Status code to return.
    :param body: Response body, in it's proper format (CSV, PDF, JSON etc.)
    :returns: Flask Response Object
    """
    response_hdrs = {'Content-Type': CONTENT_TYPE_JSON}
    response_hdrs.update(headers or {})

    args = dict(sort_keys=True, indent=4, separators=(',', ': '))
    body = json.dumps(body, **args)

    response = flask.Response(body)
    response.status_code = response_code

    for header, value in response_hdrs.items():
        response.headers.add(header, value)
    return response


def success(body=None):
    """
    Creates a hashed success response
    :param body: Response body
    :return: Flask Response Object
    """
    return make_response_object({'data': body}, response_code=200)

def not_found(body=None):
    """
    Creates a hashed not found response
    :param body: Response body
    :return: Flask Response Object
    """
    return make_response_object({'error': body}, response_code=404)

def malformed(body=None):
    """
    Creates a hashed not found response
    :param body: Response body
    :return: Flask Response Object
    """
    return make_response_object({'error': body}, response_code=400)
