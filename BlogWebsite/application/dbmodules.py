from datetime import datetime
from .extensions import db


# data tables in sqlite database start here

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String())
    date = db.Column(db.DateTime, default=datetime.now)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(255))
    author = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=None)

# data tables for sqlite database end here
