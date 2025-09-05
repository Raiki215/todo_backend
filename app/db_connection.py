import os
import psycopg2

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PW")
dbname = os.getenv("DB_NAME")

def get_connection():
    if not all([host, user, password, dbname]):
        print("警告: 一部の環境変数が未設定です")
        print(f"DB_HOST: {host or '未設定'}")
        print(f"DB_USER: {user or '未設定'}")
        print(f"DB_PW: {'設定済み' if password else '未設定'}")
        print(f"DB_NAME: {dbname or '未設定'}")
        return None
    try:
        conn = psycopg2.connect(
            host=host,
            database=dbname,
            user=user,
            password=password
        )
        return conn
    except Exception as e:
        print(f"データベース接続エラー: {e}")
        return None