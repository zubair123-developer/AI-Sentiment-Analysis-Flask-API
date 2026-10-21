import os
import sqlite3
from functools import wraps

import jwt
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from transformers import pipeline

load_dotenv()
app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')
API_USERNAME = os.getenv('API_USERNAME')
API_PASSWORD = os.getenv('API_PASSWORD')
DATABASE = 'sentiment.db'

if not all([SECRET_KEY, API_USERNAME, API_PASSWORD]):
    raise RuntimeError('Create .env with SECRET_KEY, API_USERNAME and API_PASSWORD (see .env.example)')

# The Hugging Face model is downloaded automatically on first use.
model = None


def get_model():
    global model
    if model is None:
        model = pipeline('sentiment-analysis', model='distilbert/distilbert-base-uncased-finetuned-sst-2-english')
    return model


def init_db():
    with sqlite3.connect(DATABASE) as connection:
        connection.execute('''CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            score REAL NOT NULL
        )''')


def token_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'Missing Bearer token'}), 401
        token = auth[7:]
        try:
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return function(*args, **kwargs)
    return wrapper


@app.get('/')
def home():
    return jsonify({'message': 'Sentiment Analysis API is running'})


@app.post('/login')
def login():
    data = request.get_json(silent=True) or {}
    if data.get('username') != API_USERNAME or data.get('password') != API_PASSWORD:
        return jsonify({'error': 'Wrong username or password'}), 401
    from datetime import datetime, timedelta, timezone
    token = jwt.encode({'sub': API_USERNAME, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token})


@app.post('/analyze')
@token_required
def analyze():
    data = request.get_json(silent=True) or {}
    text = data.get('text')
    if not isinstance(text, str) or not text.strip():
        return jsonify({'error': 'Provide non-empty text'}), 400
    if len(text) > 500:
        return jsonify({'error': 'Text must be 500 characters or less'}), 400
    prediction = get_model()(text)[0]
    sentiment = prediction['label']
    score = round(float(prediction['score']), 4)
    with sqlite3.connect(DATABASE) as connection:
        connection.execute('INSERT INTO predictions (text, sentiment, score) VALUES (?, ?, ?)', (text, sentiment, score))
    return jsonify({'text': text, 'sentiment': sentiment, 'score': score})


@app.get('/history')
@token_required
def history():
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute('SELECT id, text, sentiment, score FROM predictions ORDER BY id DESC').fetchall()
    return jsonify([dict(row) for row in rows])


init_db()

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)