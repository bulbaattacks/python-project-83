import secrets

import psycopg2
from flask import Flask, render_template, flash, \
    url_for, request, redirect
import os
from dotenv import load_dotenv
import validators

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_urlsafe(16))

DATABASE_URL = os.getenv('DATABASE_URL')


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(open("database.sql", "r").read())
    cur.execute('SELECT * FROM urls')
    result = cur.fetchall()
    return render_template('all_urls.html', data=result)


@app.post('/urls')
def add_url():
    data = request.form.get("url")
    if not validators.url(data) or len(data) > 255:
        flash("Некорректный URL", "danger")
        if not data:
            flash("URL обязателен", "danger")
        return render_template('index.html', data=data), 422

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(open("database.sql", "r").read())
    cur.execute('SELECT * FROM urls WHERE urls.name = %s', (data,))
    result = cur.fetchone()
    conn.commit()

    if not result:
        cur.execute('INSERT INTO urls (name) VALUES (%s)', (data,))
        cur.execute('SELECT id FROM urls WHERE urls.name = %s', (data,))
        id = cur.fetchone()
        conn.commit()
        flash("Страница успешно добавлена", "success")
        cur.close()
        conn.close()
        return redirect(url_for("show_url", id=id))
    id = result[0]
    flash("Страница уже существует", "info")
    cur.close()
    conn.close()
    return redirect(url_for("show_url", id=id))


@app.get('/urls/<int:id>')
def show_url(id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(open("database.sql", "r").read())
    cur.execute('SELECT * FROM urls WHERE urls.id = %s', (id,))
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return render_template('show.html', data=result)
