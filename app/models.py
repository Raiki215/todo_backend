from flask_login import UserMixin
from werkzeug.security import check_password_hash
from .db_connection import get_connection

class User(UserMixin):
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

        # UserMixinの実装に必要なidプロパティ
        self.id = user_id  # Flask-Loginが.idプロパティを使うので追加

    @staticmethod
    def get(user_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, name, email, password FROM users WHERE user_id = %s", (user_id,))
            row = cursor.fetchone()
            if row:
                return User(*row)
            return None
        except Exception as e:
            print(f"ユーザー取得エラー: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    #パスワードのチェック
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_by_email(email):
        conn = get_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            #メールアドレスからユーザーを取得
            cursor.execute("SELECT user_id, name, email, password FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                return User(user_id=user[0], name=user[1], email=user[2], password=user[3])
            return None
        except Exception as e:
            print(f"ユーザー取得エラー: {e}")
            return None
        finally:
            cursor.close()
            conn.close()