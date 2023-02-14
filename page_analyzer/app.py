import secrets
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, flash, \
    url_for, request, redirect
import os
from dotenv import load_dotenv
from page_analyzer.url import validate
from page_analyzer.parser import prepare_seo_data


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_urlsafe(16))

DATABASE_URL = os.getenv('DATABASE_URL')


def get_conn():
    return psycopg2.connect(DATABASE_URL)


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    conn = get_conn()
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
    conn.close()
    return render_template('all_urls.html', all_urls=result)


@app.post('/urls')
def add_url():
    data = request.form.get("url")
    errors = validate(data)
    if errors:
        return render_template('index.html', not_correct_data=data), 422
    conn = get_conn()
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM urls WHERE urls.name = %s', (data,))
        result = curs.fetchone()
    conn.commit()
    if not result:
        with conn.cursor() as curs:
            curs.execute('INSERT INTO urls (name) VALUES (%s)', (data,))
            curs.execute('SELECT id FROM urls WHERE urls.name = %s', (data,))
            id = curs.fetchone()[0]
        conn.commit()
        flash("Страница успешно добавлена", "success")
        conn.close()
        return redirect(url_for("show_url", id=id))
    id = result[0]
    flash("Страница уже существует", "info")
    conn.close()
    return redirect(url_for("show_url", id=id))


@app.get('/urls/<int:id>')
def show_url(id):
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute('''
                SELECT id, name, DATE(created_at) as created_at
                FROM urls WHERE urls.id = %s
                ''', (id,))
        result = curs.fetchone()
    if not result:
        curs.close()
        conn.close()
        return render_template('404.html'), 404
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute('''
            SELECT id, status_code, h1,
            title, description, DATE(created_at) as created_at, url_id
            FROM url_checks
            WHERE url_checks.url_id = %s
            ORDER BY id DESC''', (id,))
        check = curs.fetchall()
    conn.commit()
    conn.close()
    return render_template('show.html', check_url=check, show_url=result)


@app.post('/urls/<id>/checks')
def check_url(id):
    conn = get_conn()
    with conn.cursor() as curs:
        curs.execute('SELECT name FROM urls WHERE urls.id = %s', (id,))
        name = curs.fetchone()[0]
    try:
        parser = prepare_seo_data(name)
        status_code = parser.get('status_code')
        h1 = parser.get('h1')
        title = parser.get('title')
        description = parser.get('description')
        with conn.cursor() as curs:
            curs.execute('''
                INSERT INTO url_checks
                (url_id, status_code, h1, title, description)
                VALUES (%s, %s, %s, %s, %s)''',
                         (id, status_code, h1, title, description,))
        conn.commit()
        flash("Страница успешно проверена", "success")
    except Exception:
        flash("Произошла ошибка при проверке", "danger")
    conn.close()
    return redirect(url_for('show_url', id=id))
