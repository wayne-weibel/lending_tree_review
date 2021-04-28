# Lending Tree Reviews

## Challenge
Create an API service that collects and returns reviews found from the website Lending Tree.

## Requirements:

1. Please write the project in Ruby or Python.
2. Service should return JSON
3. The project and steps below should use this website: https://www.lendingtree.com/reviews
4. API service should accept inbound requests that contain a target Lending Tree URL to collect reviews from
    * one example of such a Lending Tree URL: https://www.lendingtree.com/reviews/personal/first-midwest-bank/52903183
5. The service should collect all 'reviews' from the target URL
6. The service should provide a response with the found reviews, containing the following:
    * title of the review
    * the content of review
    * author
    * star rating
    * date of review
    * and any other info you think would be relevant
7. The service should handle errors and bad requests
8. Write tests for your API service
9. Storing reviews for future retrieval is not necessary

__*to be complete within 72 hours*__

---

### Flask

Simple Flask setup; a single resource path, some utility functions to keep things a little cleaner.
There is room for improvement, but could spend months on it; abstraction of the response and error handling,
response body transformation, further request validation, etc.  The resource paths, if more than a handful,
are better to be added via a decorator on the class.

To use:

```
cd [path-to-repo]
make
make run

* In your favorite browser go to `http://localhost:8019/api/review?url=`
* supply a lending tree url in the param 'url'
```

Running tests:

```
cd [path-to-repo]
make
make test

* Coverage report generated to [path-to-repo]/htmlcov
```
