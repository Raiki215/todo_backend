from flask import Flask, jsonify , render_template#renderは後程消す
from .db_connection import get_connection
from .register import register_user
from flask_cors import CORS
from flask_login import LoginManager, login_required
from .login import login, logout
import os
from .models import User

# 動作確認後で消す
login_user = None


def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv('SECRET_KEY', 'dev_secret_key_for_testing')

    print(f"Secret key is set: {app.secret_key is not None}")


    CORS(app, supports_credentials=True)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"error": "認証が必要です"}), 401


    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @app.route('/')
    def home():
        conn = get_connection()
        if conn:
            return "Hello, Flask!"


    @app.route('/register', methods=['POST'])
    def register_route():
        return register_user()

    @app.route('/login', methods=['POST'])
    def login_route():
        return login()

    @app.route('/logout', methods=['POST'])
    def logout_route():
        return logout()
    
    # 動作確認用後で消す
    @app.route('/test')
    def test():
        conn = get_connection()
        if conn:
            return render_template('test.html', name="Alice")
        return "Database connection failed", 500

    return app
