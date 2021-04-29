"""
service access point
"""
import datetime
import re
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup
import flask
import flask_restful
import requests

from service.util import success, not_found, malformed, STARS_RGX, DATE_PARSE

class ReviewRequestHandler(flask_restful.Resource):
    """
    Request handler that gets the reviews
    """

    def get(self):
        """
        Returns a list of reviews for the supplied url
        :return: a list of reviews
        """
        url = flask.request.args.get('url')
        if not url:
            return malformed('"URL" parameter required')

        try:
            url = urlparse(url)
            if url.netloc != 'www.lendingtree.com':
                raise ValueError

            path = [p for p in url.path.split('/') if p]
            if len(path) != 4 or path[0] != 'reviews' or not int(path[-1]):
                raise ValueError
        except ValueError:
            return malformed('Invalid Lending Tree URL')

        url = urlunparse(url)
        html = requests.get(url)
        if html.status_code != 200:
            return not_found('{} was Not Found'.format(url))

        soup = BeautifulSoup(html.text, 'html.parser')
        reviews = soup.find_all('div', class_='mainReviews')
        if not reviews:
            return not_found('No Reviews were Found')

        data = {'url': url, 'reviews': self.__review_data(reviews)}
        return success(data)

    def __review_data(self, reviews):
        """
        parse the desired data for each review
        """
        # pylint: disable=no-self-use
        review_data = {
                'title': '',
                'content': '',
                'author': '',
                'date': '',
                'stars': {'score': 0, 'out_of': 0},
                'points': {}
            }
        review_list = []
        for review in reviews:
            parsed = review_data.copy()

            details = review.select_one('div.reviewDetail')
            parsed['title'] = details.select_one('p.reviewTitle').text.strip()
            parsed['content'] = details.select_one('p.reviewText').text.strip()

            # author text is not a real name 'XXXX from City, State'
            author = details.select_one('p.consumerName').text
            parsed['author'] = re.sub(r'\s+', ' ', author.strip())

            # date parse should be configurable
            date = details.select_one('p.consumerReviewDate').text
            parsed['date'] = datetime.datetime.strptime(date, DATE_PARSE).date().isoformat()

            # regex should be configurable
            stars = review.select_one('div.starReviews > div.recommended > div.numRec')
            stars = re.compile(STARS_RGX).match(stars.text)
            parsed['stars']['score'] = int(stars.group(1))
            parsed['stars']['out_of'] = int(stars.group(2))

            points = review.select('div.reviewPoints ul li')
            for point in points:
                field = re.sub(r'\s+', ' ', point.p.text.strip().strip(':'))
                value = point.div.text.strip()
                parsed['points'][field] = value

            review_list.append(parsed)

        return review_list
