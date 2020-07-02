import os
from functools import wraps
from flask import Blueprint
from passlib.hash import sha256_crypt
from flask import render_template, flash, redirect, session, url_for, logging, request

# developer define imports

from .dbConnection import get_connection
from .extensions import db
from .dbmodules import User, Articles
from .forms import RegisterForm, ArticlesForm


base_dir = os.path.abspath(os.path.dirname(__file__))

server = Blueprint("main", __name__)


# authentication wrapper for user
def is_accessible(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)

        flash('Unauthorised access, please log in.', 'danger')
        return redirect(url_for('main.user_login'))
    return wrapped


# user register route
@server.route('/register', methods=['GET', 'POST'])
def user_register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        password = sha256_crypt.hash(form.password.data)
        # with server.app_context():
        conn = get_connection('db.sqlite3')
        cur = conn.cursor()
        query = '''insert into user(name, username, email, password) values(?,?,?,?);'''
        cur.execute(query, (form.name.data, form.username.data, form.email.data, password))
        conn.commit()
        conn.close()
        # user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=password)

        flash('You are now registered and can log in.', 'success')
        return render_template('home.html')
    return render_template('register.html', form=form)


# user login route
@server.route('/login', methods=['GET', 'POST'])
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
                # server.logger.info("PASSWORD MATCHED")
                session['logged_in'] = True
                session['username'] = username
                flash("You are logged in ", 'success')
                return redirect(url_for('main.user_dashboard'))

            # server.logger.info("PASSWORD DO NOT MATCH")
            error = 'Invalid Login'
            return render_template('login.html', error=error)
        cur.close()

        # server.logger.info("NO USER")
        error = 'User not found'
        return render_template('login.html', error=error)

    return render_template('login.html')


@server.route('/home')
def index():
    return render_template('home.html')


@server.route('/about')
def about():
    return render_template('about.html')


# route for all articles
@server.route('/articles')
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
@server.route('/add_article', methods=['GET', 'POST'])
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
@server.route('/edit_article/<string:ids>/', methods=["GET", 'POST'])
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


@server.route('/delete_article/<string:ids>/')
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
@server.route('/article/<string:ids>/')
def show_article(ids):
    conn = get_connection("db.sqlite3")
    cur = conn.cursor()
    query = '''select * from articles where id = ?'''
    cur.execute(query, (ids,))
    records = cur.fetchall()

    if len(records) > 0:
        return render_template('article.html', current_article=records)

    flash("No article found.", 'danger')
    return redirect(url_for('main.all_articles'))

    # current_article = Articles.query.filter_by(id=ids).first()
    # return render_template('article.html', current_article=current_article)


# route for user dashboard
@server.route('/dashboard')
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
@server.route('/logout')
@is_accessible
def user_logout():
    session.clear()
    flash('You are logged out now.', 'success')
    return redirect(url_for('main.user_login'))

