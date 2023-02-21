import secrets
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, flash, \
    url_for, request, redirect, session
import os
from dotenv import load_dotenv
from page_analyzer.url import validate
from page_analyzer.parser import prepare_seo_data

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_urlsafe(16))

DATABASE_URL = os.getenv('DATABASE_URL')


@app.before_request
def init_db_connection():
    if session.get('count') is None:
        conn = get_conn()
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(open("database.sql", "r").read())
        session['count'] = 0


def get_conn():
    return psycopg2.connect(DATABASE_URL)


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    conn = get_conn()
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
                '''
                SELECT urls.id, urls.name, url_checks.status_code,
                DATE(url_checks.created_at)
                FROM urls
                LEFT JOIN url_checks on urls.id=url_checks.url_id
                AND url_checks.created_at =
                    (SELECT MAX(created_at)
                        FROM url_checks
                        WHERE url_id = urls.id)
                ORDER BY urls.id DESC
                ''')
            result = curs.fetchall()
    return render_template('all_urls.html', all_urls=result)


@app.post('/urls')
def add_url():
    data = request.form.get("url")
    errors = validate(data)
    if errors:
        for error in errors:
            flash(error, "danger")
        return render_template('index.html', not_correct_data=data), 422
    conn = get_conn()
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) \
                as curs:
            curs.execute('SELECT * FROM urls WHERE urls.name = %s', (data,))
            result = curs.fetchone()
        if not result:
            with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) \
                    as curs:
                curs.execute('INSERT INTO urls (name) VALUES (%s)', (data,))
                curs.execute('SELECT id FROM urls WHERE urls.name = %s',
                             (data,))
                id = curs.fetchone().id
            flash("Страница успешно добавлена", "success")
            return redirect(url_for("show_url", id=id))
        id = result.id
        flash("Страница уже существует", "info")
    return redirect(url_for("show_url", id=id))


@app.get('/urls/<int:id>')
def show_url(id):
    conn = get_conn()
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute('''
                    SELECT id, name, DATE(created_at) as created_at
                    FROM urls WHERE urls.id = %s
                    ''', (id,))
            result = curs.fetchone()
        if not result:
            return render_template('404.html'), 404
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute('''
                SELECT id, status_code, h1,
                title, description, DATE(created_at) as created_at, url_id
                FROM url_checks
                WHERE url_checks.url_id = %s
                ORDER BY id DESC''', (id,))
            check = curs.fetchall()
    return render_template('show.html', check_url=check, show_url=result)


@app.post('/urls/<id>/checks')
def check_url(id):
    conn = get_conn()
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) \
                as curs:
            curs.execute('SELECT name FROM urls WHERE urls.id = %s', (id,))
            name = curs.fetchone().name
        try:
            prepared_data = prepare_seo_data(name)
            status_code = prepared_data.get('status_code')
            h1 = prepared_data.get('h1')
            title = prepared_data.get('title')
            description = prepared_data.get('description')
            with conn.cursor() as curs:
                curs.execute('''
                    INSERT INTO url_checks
                    (url_id, status_code, h1, title, description)
                    VALUES (%s, %s, %s, %s, %s)''',
                             (id, status_code, h1, title, description,))
            flash("Страница успешно проверена", "success")
        except Exception:
            flash("Произошла ошибка при проверке", "danger")
    return redirect(url_for('show_url', id=id))
