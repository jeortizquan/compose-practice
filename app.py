import time
import redis
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return '<h1>Python SQL Lite Demo Hello World!</h1><br>' \
           'I have been visited <strong>{}</strong> times. <br>\n' \
           '<em>usage</em><br>' \
           '/api/v1/resources/authors/all<br>' \
           '/api/v1/resources/quotes/all<br>'.format(count)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/api/v1/resources/authors/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('quotes.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM authors;').fetchall()
    return jsonify(all_books)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404