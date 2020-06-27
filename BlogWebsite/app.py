import os
from data import articles
from functools import wraps
from datetime import datetime
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask import Flask, render_template, flash, redirect, session, url_for, logging, request

# developer define imports
from dbConnection import get_connection

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(base_dir, "db.sqlite3")


db = SQLAlchemy(app)


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


# user registration form class
class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=1, max=50)])
    username = StringField('User name', [validators.length(min=4, max=25)])
    email = StringField('Email', [validators.length(min=6, max=50)])
    password = PasswordField('Password',
                             [validators.DataRequired(),
                              validators.EqualTo('confirm', message='Password do not match')])
    confirm = PasswordField('Confirm password')


# user articles from class
class ArticlesForm(Form):
    title = StringField('Title', [validators.length(min=2, max=200)])
    body = TextAreaField('Body', [validators.length(min=20)])


# authentication wrapper for user
def is_accessible(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)

        flash('Unauthorised access, please log in.', 'danger')
        return redirect(url_for('user_login'))
    return wrapped


# user register route
@app.route('/register', methods=['GET', 'POST'])
def user_register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        password = sha256_crypt.hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=password)
        db.session.add(user)
        db.session.commit()

        flash('You are now registered and can log in.', 'success')
        return render_template('home.html')
    return render_template('register.html', form=form)


# user login route
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        # getting form field
        username = request.form.get('username', None)
        password = request.form['password']

        # data = User.query.filter_by(username=username).first()
        conn = get_connection("db.sqlite3")
        cur = conn.cursor()
        query = '''SELECT password FROM user WHERE username = ?;'''
        cur.execute(query, (username,))
        data = cur.fetchall()
        print(data)
        if len(data) > 0:
            if sha256_crypt.verify(password, data[0][0]):
                app.logger.info("PASSWORD MATCHED")
                session['logged_in'] = True
                session['username'] = username
                flash("You are logged in ", 'success')
                return redirect(url_for('user_dashboard'))

            app.logger.info("PASSWORD DO NOT MATCH")
            error = 'Invalid Login'
            return render_template('login.html', error=error)
        cur.close()

        app.logger.info("NO USER")
        error = 'User not found'
        return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


# route for all articles
@app.route('/articles')
@is_accessible
def all_articles():
    if session.get("logged_in"):
        conn = get_connection('db.sqlite3')
        cur = conn.cursor()
        query = '''select id, author, title from articles;'''
        cur.execute(query)
        records = cur.fetchall()
        if len(records) > 0:
            return render_template('articles.html', articles=records)
    flash('Session time out, please log in again.', 'success')
    return redirect(url_for('user_login'))


# route for add article
@app.route('/add_article', methods=['GET', 'POST'])
@is_accessible
def add_article():
    form = ArticlesForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        body = form.body.data
        author = session.get('username')

        article = Articles(title=title, body=body, author=author)
        db.session.add(article)
        db.session.commit()

        flash('Article added', 'success')

        return redirect(url_for('user_dashboard'))
    return render_template('add_article.html', form=form)


# route for edit article
@app.route('/edit_article/<string:ids>/', methods=["GET", 'POST'])
@is_accessible
def edit_article(ids):
    # current_article = Articles.query.filter_by(id=ids).first()
    conn = get_connection('db.sqlite3')
    cur = conn.cursor()
    query = '''select title, body from articles where id = ?'''
    cur.execute(query, (ids,))
    records = cur.fetchall()

    form = ArticlesForm(request.form)
    form.title.data = records[0][0]
    form.body.data = records[0][1]

    # form.title.data = current_article.title
    # form.body.data = current_article.body

    if request.method == "POST" and form.validate():
        title = request.form.get('title')
        body = request.form.get("body")
        # conn = get_connection('db.sqlite3')
        query = '''UPDATE articles SET title = ?, body=? WHERE id = ?;'''
        cur = conn.cursor()
        cur.execute(query, (title, body, ids))
        conn.commit()

        flash('Article updated', 'success')
        conn.close()
        return redirect(url_for('user_dashboard'))
    conn.close()
    return render_template('add_article.html', form=form)


@app.route('/delete_article/<string:ids>/')
@is_accessible
def delete_article(ids):
    conn = get_connection('db.sqlite3')
    cur = conn.cursor()
    query = '''DELETE FROM articles WHERE id = ?'''
    cur.execute(query, (ids,))
    conn.commit()
    conn.close()

    flash("Article deleted", 'success')
    return redirect(url_for('user_dashboard'))


# route for show article to user
@app.route('/article/<string:ids>/')
def show_article(ids):
    current_article = Articles.query.filter_by(id=ids).first()
    return render_template('article.html', current_article=current_article)


# route for user dashboard
@app.route('/dashboard')
@is_accessible
def user_dashboard():
    conn = get_connection('db.sqlite3')
    cur = conn.cursor()
    query = '''select * from articles where author = ?'''
    cur.execute(query, (session.get('username'),))
    records = cur.fetchall()
    # user_articles = Articles.query.all()
    if len(records)>0:
        return render_template('dashboard.html', articles=records)
    msg = 'No article found'
    return render_template('dashboard.html', msg=msg)


# route for user logout
@app.route('/logout')
@is_accessible
def user_logout():
    session.clear()
    flash('You are logged out now.', 'success')
    return redirect(url_for('user_login'))


if __name__ == "__main__":
    app.secret_key = "secretkey12345"
    app.run(debug=True)
