import csv
import io

import requests
import flask

from . import db
from . import models

REVIEWS_CVS_URL = 'https://docs.google.com/spreadsheet/ccc?key=1iSR0bR0TO5C3CfNv-k1bxrKLD5SuYt_2HXhI2yq15Kg&output=csv'
PRODUCTS_CSV_URL = 'https://docs.google.com/spreadsheet/ccc?key=1roypo_8amDEIYc-RFCQrb3WyubMErd3bxNCJroX-HVE&output=csv'

bp = flask.Blueprint('scripts', __name__)


@bp.cli.command('boostrap_db')
def bootstrap_db():
    """Заливка базы данных.

    Использовать: flask scripts bootstrap_db
    """
    # Заливка продуктов в базу данных
    products_content = requests.get(PRODUCTS_CSV_URL).content.decode()
    products_reader = csv.DictReader(io.StringIO(products_content))

    for row in products_reader:
        product = models.Product(title=row['Title'], asin=row['Asin'])
        db.session.add(product)
    db.session.commit()

    # Заливка отзывов в базу данных
    reviews_content = requests.get(REVIEWS_CVS_URL).content.decode()
    reader_reviews = csv.DictReader(io.StringIO(reviews_content))
    for row in reader_reviews:
        review = models.Review(title=row['Title'], asin=row['Asin'], content=row['Review'])
        db.session.add(review)
    db.session.commit()

    print('Заливка завершена')
