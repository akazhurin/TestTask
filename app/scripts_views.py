import csv
import io

import requests
import flask

from . import db
from . import models

REVIEWS_CVS_URL = 'https://docs.google.com/spreadsheet/ccc?key=1iSR0bR0TO5C3CfNv-k1bxrKLD5SuYt_2HXhI2yq15Kg&output=csv'
PRODUCTS_CSV_URL = 'https://docs.google.com/spreadsheet/ccc?key=1roypo_8amDEIYc-RFCQrb3WyubMErd3bxNCJroX-HVE&output=csv'

bp = flask.Blueprint('scripts', __name__)


@bp.cli.command('bootstrap_db')
def bootstrap_db():
    """fill db.

    for use: flask scripts bootstrap_db
    """
    # Uploading products to the database
    products_content = requests.get(PRODUCTS_CSV_URL).content.decode()
    products_reader = csv.DictReader(io.StringIO(products_content))

    for row in products_reader:
        product = models.Product(title=row['Title'], asin=row['Asin'])
        db.session.add(product)
    db.session.commit()

    # Uploading reviews to the database
    reviews_content = requests.get(REVIEWS_CVS_URL).content.decode()
    reader_reviews = csv.DictReader(io.StringIO(reviews_content))
    for row in reader_reviews:
        review = models.Review(title=row['Title'], asin=row['Asin'], content=row['Review'])
        db.session.add(review)
    db.session.commit()

    print('Upload completed')
