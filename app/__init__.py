from flask import Flask, jsonify , render_template#renderは後程消す
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
from .get_todos import getAll_todos, getCompleted_todos, getNotYet_todos,high_priority
from .edit_todos import edit_todo_all, finish_flg_OnOff, tomorrow_todo
from .delete_todo import del_Todo
from .notification import get_notification_history, read_notification, delete_notification

load_dotenv()

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
    
    # userの全てのtodoを取得　
    @app.route('/get_user_todos', methods=['GET'])
    @login_required
    def get_user_todos_route():
        return getAll_todos()
    
    # 完了済みfinish_flg=TRUE 
    @app.route('/get_user_todos_finished', methods=['GET'])
    @login_required
    def get_user_todos_finished_route():
        return getCompleted_todos()
    
    #まだ完了していないtodo 
    @app.route('/get_user_todos_yet', methods=['GET'])
    @login_required
    def get_user_todos_yet_route():
        return getNotYet_todos()
    
    # 優先度3以上のものだけ
    @app.route('/get_user_todos_highpriority', methods=['GET'])
    @login_required
    def get_user_todos_highpriority_route():
        return high_priority()
    
    # 編集（更新）
    @app.route('/get_user_todos_update', methods=['POST'])
    @login_required
    def get_user_todos_update_route():
        return edit_todo_all()
    
    # finishflgのonoff
    @app.route('/get_user_todos_finishflg_update', methods=['POST'])
    @login_required
    def get_user_todos_update_finishflg_route():
        return finish_flg_OnOff()
    
    # 削除
    @app.route('/get_user_todos_delete', methods=['POST'])
    @login_required
    def get_user_todos_delete_route():
        return del_Todo()

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

    @app.route('/tomorrow_todo', methods=['GET'])
    @login_required
    def tomorrow_todo_route():
        return tomorrow_todo()
    return app
