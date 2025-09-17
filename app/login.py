from flask import request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .db_connection import get_connection

def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "メールアドレスとパスワードは必須です"}), 400

    user = User.get_by_email(email)
    if not user or not user.check_password(password):
        return jsonify({"error": "メールアドレスまたはパスワードが無効です"}), 401

    #ログイン成功でユーザー保存
    login_user(user)

    return jsonify({
        "message": "ログインに成功しました",
        "user": {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email
        }
    }), 200

def logout():
    if current_user.is_authenticated:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE users
            SET push_subscription = NULL
            WHERE user_id = %s
        """, (current_user.user_id,))
        conn.commit()
        cur.close()
        conn.close()
    #ログアウト
    logout_user()
    session.clear()
    return jsonify({"message": "ログアウト成功"}),200