from flask import Flask
from .db_connection import get_connection
from .register import register_user
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # CORSを有効化
    CORS(app)

    @app.route('/')
    def home():
        conn = get_connection()
        if conn:
            return "Hello, Flask!"
        return "Database connection failed", 500

    # ユーザー登録
    @app.route('/register', methods=['POST'])
    def register_route():
        return register_user()

    return app