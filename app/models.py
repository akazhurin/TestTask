from . import db


class Product(db.Model):
    """Product model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    asin = db.Column(db.String(50), unique=True, index=True)
    reviews = db.relationship('Review', backref='product', lazy='dynamic')


class Review(db.Model):
    """Review model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    asin = db.Column(db.String(50), db.ForeignKey('product.asin', ondelete='cascade'))
