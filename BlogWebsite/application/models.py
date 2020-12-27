from datetime import datetime
from .extensions import db
from sqlalchemy import Column, Integer, String, DateTime, Boolean


# data tables in sqlite database start here


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    username = Column(String(50))
    role = Column(String(10))
    email = Column(String(60))
    password = Column(String(50))
    date = Column(DateTime, default=datetime.now)

    def __init__(self, name=None, email=None, username=None, password=None, role=None):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return "{}; {}; {}".format(self.id, self.name, self.username)


class Articles(db.Model):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer)
    title = Column(String(100))
    article_status = Column(String(10))
    body = Column(String(255))
    author = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=None)

    def __init__(self, title, author, author_id, article_status, body, created_at, update_at):
        self.title = title
        self.author = author
        self.author_id = author_id
        self.article_status = article_status
        self.body = body
        self.created_at = created_at
        self.update_at = update_at

    def __repr__(self):
        return "{}; {}; {}".format(self.id, self.title, self.author)

# data tables for sqlite database end here
