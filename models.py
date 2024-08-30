from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TEXT

db = SQLAlchemy()

class Request(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    products = db.relationship('Product', backref='request', lazy=True)

class Product(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    serial_number = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    input_image_urls = db.Column(TEXT, nullable=False)
    output_image_urls = db.Column(TEXT)
    request_id = db.Column(db.String(36), db.ForeignKey('request.id'), nullable=False)
