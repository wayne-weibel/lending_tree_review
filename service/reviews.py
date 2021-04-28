"""
service access point
"""
from flask import request
import flask_restful

from service.util import success

class ReviewRequestHandler(flask_restful.Resource):
    """
    Request handler that gets the reviews
    """
    # pylint: disable=R0201

    def get(self):
        """
        Returns a list of the account team roles
        :return: a list of the account team roles
        """

        data = {'data': [1, 2, 3], 'args': request.args}
        print(data)
        return success(data)
