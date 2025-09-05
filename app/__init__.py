from flask import Flask
from .db_connection import get_connection

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        conn = get_connection()
        if conn:
            return "Hello, Flask!"
        return "Database connection failed", 500
    return app