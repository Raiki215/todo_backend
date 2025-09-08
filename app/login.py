from flask import request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from .models import User

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
    }), 200

def logout():
    #ログアウト
    logout_user()
    session.clear()
    return jsonify({"message": "ログアウト成功"}),200