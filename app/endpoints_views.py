import flask
from flask_paginate import Pagination, request

from . import cache, db
from . import models

bp = flask.Blueprint('Endpoints', __name__)

@bp.get('/api/v1/products/<int:product_id>/')
@bp.get('/api/v1/products/<int:product_id>/<int:page>')
@cache.memoize()
def products(product_id, page=1):
    """Получение продукта и отзывов по product ID"""
    # Поиск продукта в БД
    product = models.Product.query.get(product_id)
    if not product:
        flask.abort(404, 'product not found')

    # Получение отзывов и создание пагинации
    reviews = models.Review.query.filter_by(asin=product.asin)

    pagination = reviews.paginate(page=page, per_page=2)

    # Генерация json ответа
    return {
               'id': product.id,
               'title': product.title,
               'asin': product.asin,
               'reviews': {
                   'has_next': pagination.has_next,
                   'has_prev': pagination.has_prev,
                   'per_page': pagination.per_page,
                   'total': pagination.total,
                   'review': [{'id': r.id, 'title': r.title,'content': r.content} for r in pagination]
               }
           }, 200

@bp.put('/api/v1/reviews/')
def reviews():
    """Создание нового отзыва"""
    # Получение аргументов с запроса
    product_id = flask.request.args.get('product_id')
    title = flask.request.args.get('title')
    content = flask.request.args.get('content')

    # Поиск продукта в БД
    product = models.Product.query.get(product_id)
    if not product:
        flask.abort(404, 'product not found')

    # Создание отзыва и сохранение в БД
    review = models.Review(title=title, content=content, asin=product.asin)
    db.session.add(review)
    db.session.commit()

    # Очистка кеша, так как продукт был обновлен
    cache.delete_memoized(products)

    # Возврат сообщения об успехе
    return {
               'message': '201'
           }, 201
