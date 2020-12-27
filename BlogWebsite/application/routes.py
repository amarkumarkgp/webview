import os
import io
import datetime
from functools import wraps
from flask import Blueprint
from passlib.hash import sha256_crypt
from flask import render_template, g, flash, redirect, session, url_for, request, make_response, jsonify

# developer define imports

# from .dbConnection import get_connection
from .extensions import mysql, db
from .forms import RegisterForm, ArticlesForm
from .models import User, Articles


base_dir = os.path.abspath(os.path.dirname(__file__))

server = Blueprint("main", __name__,
                   static_folder=os.path.join(base_dir, "static"),
                   template_folder=os.path.join(base_dir, 'templates'))


# authentication wrapper for user
def is_accessible(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if session.get('logged_in'):
            return f(*args, **kwargs)

        flash('Unauthorised access, please log in.', 'danger')
        return redirect(url_for('main.user_login'))
    return wrapped


@server.before_request
def before_request_func():
    if 'sql_cur' not in g:
        g.sql_cur = mysql.connection.cursor()


@server.after_request
def after_request_func(response):
    if g.sql_cur is not None:
        g.sql_cur.close()
    return response


@server.route('/new')
def newlogin():
    return render_template('loginnew.html')


# user register route
@server.route('/register', methods=['GET', 'POST'])
def user_register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        password = form.password.data #sha256_crypt.encrypt(form.password.data)
        # query = '''insert into users(name, username, email, password) values(%s,%s,%s,%s);'''
        # g.sql_cur.execute(query, [form.name.data, form.username.data, form.email.data, password])
        # g.sql_connn.commit()
        new_user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=password)
        db.session.add(new_user)
        db.session.commit()

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
        user = User.query.filter(User.username == username).first()

        if user:
            if password == user.password:
                session['logged_in'] = True
                session['username'] = username
                session['userid'] = user.id
                session['role'] = user.role
                flash("You are logged in ", 'success')
                return render_template('home.html')

            error = 'Invalid Login'
            return render_template('login.html', error=error)

        # server.logger.info("NO USER")
        error = 'User not found'
        return render_template('login.html', error=error)

    return render_template('login.html')


@server.route('/')
@server.route('/index')
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
    if session.get("logged_in") is not None:
        query = f"select id, author, title from articles where article_status = 'a' "
        records = Articles.query.filter_by(article_status='a').all()
        # g.sql_cur.execute(query)
        # records = g.sql_cur.fetchall()
        if records:
            return render_template('articles.html', articles=records)
        flash("There are no articles.")
        return render_template('articles.html')
    flash('Session time out, please log in again.', 'success')
    return redirect(url_for('main.user_login'))


# route for add article
@server.route('/add_article', methods=['GET', 'POST'])
@is_accessible
def add_article():
    form = ArticlesForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        body = form.body.data
        articlestatus = form.articlestatus.data
        author = session.get('username')
        author_id = session.get('userid')

        # query = '''INSERT INTO articles(title, body, author, author_id, article_status) VALUES(%s, %s, %s, %s, %s);'''
        new_article = Articles(title=title,
                               author=author,
                               author_id=author_id,
                               article_status=articlestatus,
                               body=body,
                               created_at=None,
                               update_at=None
                               )
        db.session.add(new_article)
        db.session.commit()
        flash('Article added', 'success')

        return redirect(url_for('main.user_dashboard'))
    return render_template('add_article.html', form=form)


# route for edit article
@server.route('/edit_article/<string:ids>/', methods=["GET", 'POST'])
@is_accessible
def edit_article(ids):
    query = '''select title, body from articles where id = %s'''
    g.sql_cur.execute(query, [ids, ])
    records = g.sql_cur.fetchone()

    form = ArticlesForm(request.form)
    print(records, type(records))
    form.title.data = records.get('title')
    form.body.data = records.get('body')
    print('reached at 176')

    if request.method == "POST" and form.validate():
        title = request.form.get('title')
        body = request.form.get("body")
        articlestatus = request.form.get('articlestatus')
        update_time = datetime.datetime.now()
        article = Articles.query.filter_by(id=ids).first()
        article.title = title
        article.body = body
        article.article_status = articlestatus
        article.update_at = update_time

        db.session.commit()
        flash('Article updated', 'success')

        return redirect(url_for('main.user_dashboard'))
    return render_template('add_article.html', form=form)


@server.route('/delete_article/<string:ids>/')
@is_accessible
def delete_article(ids):
    Articles.query.filter_by(id=ids).delete()
    db.session.commit()

    flash("Article deleted", 'success')
    return redirect(url_for('main.user_dashboard'))


# route for show article to user
@server.route('/article/<string:ids>/')
def show_article(ids):
    query = '''select * from articles where id = %s'''
    g.sql_cur.execute(query, [ids, ])
    records = g.sql_cur.fetchone()
    if records:
        return render_template('article.html', current_article=records)

    flash("No article found.", 'danger')
    return redirect(url_for('main.all_articles'))


# route for user dashboard
@server.route('/dashboard')
@is_accessible
def user_dashboard():
    # query = '''select * from articles where author = %s'''
    records = Articles.query.filter_by(author_id=session.get('userid')).all()
    # g.sql_cur.execute(query, [session.get('username'), ])
    # records = g.sql_cur.fetchall()
    if records:
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


@server.route('/')
def landing_view():
    return make_response(jsonify({"status": "ok", "mode": "developing", "version": 101,
                                  'uri': request.url}))


