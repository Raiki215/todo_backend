from flask import Flask, jsonify
from .db_connection import get_connection
from .register import register_user
from flask_cors import CORS
from flask_login import LoginManager, login_required
from .login import login, logout
from .me import get_current_user
import os
from .models import User
from .insert_todo import ai_result, manual_save_todo
from dotenv import load_dotenv
from .send_email import send_email
from .notification import get_notification_history, read_notification, delete_notification

load_dotenv()

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

    @app.route('/me', methods=['GET'])
    @login_required
    def me_route():
        return get_current_user()

    @app.route('/insert_todo', methods=['POST'])
    @login_required
    def insert_todo():
        return ai_result()

    @app.route('/manual_insert_todo', methods=['POST'])
    @login_required
    def manual_insert_todo():
        return manual_save_todo()

    @app.route('/send_email', methods=['POST'])
    @login_required
    def send_email_route():
        return send_email()

    @app.route('/notification_history', methods=['GET'])
    @login_required
    def notification_history_route():
        return get_notification_history()

    @app.route('/read_notification', methods=['GET'])
    @login_required
    def read_notification_route():
        return read_notification()

    @app.route('/delete_notification', methods=['GET'])
    @login_required
    def delete_notification_route():
        return delete_notification()

    return app