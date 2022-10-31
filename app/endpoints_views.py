import flask
from flask_paginate import Pagination, request

from . import cache, db
from . import models

bp = flask.Blueprint('Endpoints', __name__)


@bp.get('/api/v1/products/<int:product_id>/')
@bp.get('/api/v1/products/<int:product_id>/<int:page>')
@cache.memoize()
def products(product_id, page=1):
    """Get product and reviews by product ID"""
    # Find product in the database
    product = models.Product.query.get(product_id)
    if not product:
        flask.abort(404, 'product not found')

    # Getting reviews and creating pagination
    reviews = models.Review.query.filter_by(asin=product.asin)

    pagination = reviews.paginate(page=page, per_page=2)

    # json response generation
    return {
               'id': product.id,
               'title': product.title,
               'asin': product.asin,
               'reviews': {
                   'has_next': pagination.has_next,
                   'has_prev': pagination.has_prev,
                   'per_page': pagination.per_page,
                   'total': pagination.total,
                   'review': [{'id': r.id, 'title': r.title, 'content': r.content} for r in pagination]
               }
           }, 200


@bp.put('/api/v1/reviews/')
def reviews():
    """Create a new review"""
    # Getting arguments from a request
    product_id = flask.request.args.get('product_id')
    title = flask.request.args.get('title')
    content = flask.request.args.get('content')

    # Find Product in the database
    product = models.Product.query.get(product_id)
    if not product:
        flask.abort(404, 'product not found')

    # Creating a review and saving to the database
    review = models.Review(title=title, content=content, asin=product.asin)
    db.session.add(review)
    db.session.commit()

    # Clearing the cache since the product has been updated
    cache.delete_memoized(products)

    # return success
    return {
               'message': '201'
           }, 201
