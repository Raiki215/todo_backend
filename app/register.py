from .db_connection import get_connection
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash


#ユーザー登録処理
def register_user():
    # JSONデータの取得
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    hashed_password = generate_password_hash(password)
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            # 既に登録されている場合
            return jsonify({"error": "このメールアドレスは既に登録されています"}), 409
        sql = """
        INSERT INTO users (name, email, password) VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (name, email, hashed_password))

        conn.commit()
        return jsonify({
            "message": "ユーザー登録に成功しました",
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"登録エラー: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

