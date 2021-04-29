"""reviews test cases"""
# pylint: disable=no-self-use,attribute-defined-outside-init
import json

import unittest.mock as mock

from server import APP


class TestReviewRequestHandler:
    """test review request"""

    def setup_method(self):
        '''set up tests'''
        self.valid_url = 'https://www.lendingtree.com/reviews/personal/first-midwest-bank/52903183'
        self.not_lending_tree = 'https://example.com/test'
        self.not_length = 'https://www.lendingtree.com/reviews/not-long-enough'
        self.not_reviews = 'https://www.lendingtree.com/BAD_PATH/personal/first-midwest-bank/52903183'
        self.not_number_end = 'https://www.lendingtree.com/reviews/personal/first-midwest-bank/52903183AAAA'

    def test_review_missing_param(self):
        '''test malformed request'''
        with APP.test_client() as client:
            response = client.get('/api/reviews')
        assert response.status_code == 400
        assert json.loads(response.data) == '"URL" parameter required'

    def test_review_malformed(self):
        '''test malformed request'''
        with APP.test_client() as client:
            response = client.get('/api/reviews?url={}'.format(self.not_lending_tree))
        assert response.status_code == 400
        assert json.loads(response.data) == 'Invalid Lending Tree URL'

        with APP.test_client() as client:
            response = client.get('/api/reviews?url={}'.format(self.not_length))
        assert response.status_code == 400
        assert json.loads(response.data) == 'Invalid Lending Tree URL'

        with APP.test_client() as client:
            response = client.get('/api/reviews?url={}'.format(self.not_reviews))
        assert response.status_code == 400
        assert json.loads(response.data) == 'Invalid Lending Tree URL'

        with APP.test_client() as client:
            response = client.get('/api/reviews?url={}'.format(self.not_number_end))
        assert response.status_code == 400
        assert json.loads(response.data) == 'Invalid Lending Tree URL'

    @mock.patch('service.reviews.requests')
    def test_url_not_found(self, requests):
        '''test url not found'''
        with APP.test_client() as client:
            response = client.get('/api/reviews?url={}'.format(self.valid_url))
        assert requests.get.called_with(self.valid_url)
        assert response.status_code == 404
        assert json.loads(response.data) == '{} was Not Found'.format(self.valid_url)

    @mock.patch('service.reviews.requests')
    def test_reviews_not_found(self, requests):
        '''test reviews not found'''
        response = mock.MagicMock(status_code=200, text='NO REVIEWS FOUND')
        requests.get.return_value = response
        with APP.test_client() as client:
            response = client.get('/api/reviews?url={}'.format(self.valid_url))
        assert requests.get.called_with(self.valid_url)
        assert response.status_code == 404
        assert json.loads(response.data) == 'No Reviews were Found'

    @mock.patch('service.reviews.requests')
    def test_valid_reviews(self, requests):
        '''test valid reviews'''
        response = mock.MagicMock(status_code=200, text=open('tests/valid_review.html').read())
        requests.get.return_value = response
        with APP.test_client() as client:
            response = client.get('/api/reviews?url={}'.format(self.valid_url))
        assert requests.get.called_with(self.valid_url)
        assert response.status_code == 200

        expected = {
            'reviews': [{'author': 'Ann from Tallahassee, FL',
                          'content': 'TEST REVIEW CONTEXT',
                          'date': '2021-04-01',
                          'points': {'Closed with Lender': 'Yes',
                                     'Loan Officer': 'Russell Ferrari',
                                     'Loan Type': 'Refinance',
                                     'Review Type': 'Loan Officer Review'},
                          'stars': {'out_of': 5, 'score': 3},
                          'title': 'Great Service'}],
            'url': self.valid_url
        }
        assert json.loads(response.data) == expected
