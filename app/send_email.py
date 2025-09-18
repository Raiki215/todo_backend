from flask_mail import Message, Mail
from flask import current_app, jsonify, request
from dotenv import load_dotenv
from flask_login import current_user
import os
from datetime import datetime
from .db_connection import get_connection

load_dotenv()

def send_email(user_id, todo, deadline, alert_message, app):
    """
    ユーザーIDを元にメールを送信する関数
    
    Args:
        user_id: ユーザーID
        todo: タスク名
        deadline: 締切日時
        alert_message: 通知メッセージ
        
    Returns:
        bool: 送信成功時はTrue、失敗時はFalse
    """
    print(f"メール送信処理を開始します: ユーザーID {user_id}, タスク '{todo}'")
    
    try:
        # 環境変数の取得とエラー処理の改善
        mail_server = os.getenv('MAIL_SERVER')
        mail_port = os.getenv('MAIL_PORT')
        mail_use_tls = os.getenv('MAIL_USE_TLS')
        mail_username = os.getenv('MAIL_USERNAME')
        mail_password = os.getenv('MAIL_PASSWORD')
        
        # 設定情報のログ出力 (パスワードは表示しない)
        print(f"メール設定: サーバー={mail_server}, ポート={mail_port}, TLS={mail_use_tls}, ユーザー名={mail_username}")
        
        if not all([mail_server, mail_port, mail_username, mail_password]):
            print("メール設定が不完全です")
            return False
        
        # ユーザーのメールアドレス取得
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT email FROM users WHERE user_id = %s", (user_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if not result:
            print(f"ユーザーID {user_id} のメールアドレスが見つかりません")
            return False
        
        email = result[0]
        print(f"送信先メールアドレス: {email}")
        
        # メール本文の作成
        deadline_str = deadline.strftime("%Y年%m月%d日 %H:%M") if isinstance(deadline, datetime) else str(deadline)
        
        # 渡されたFlaskアプリを使用
        try:
            if not app:
                print("有効なFlaskアプリケーションが渡されていません")
                return False
                
            # 明示的にアプリケーションコンテキストを作成
            with app.app_context():
                # メール設定
                app.config['MAIL_SERVER'] = mail_server
                app.config['MAIL_PORT'] = int(mail_port)
                app.config['MAIL_USE_TLS'] = mail_use_tls.lower() in ('true', 'yes', '1', 'on') if mail_use_tls else False
                app.config['MAIL_USERNAME'] = mail_username
                app.config['MAIL_PASSWORD'] = mail_password
                mail = Mail(app)
                
                # メッセージ作成
                msg = Message(
                    subject="ToDo通知",
                    sender=mail_username,
                    recipients=[email]
                )
                msg.body = (
                    f"タスク名: {todo}\n"
                    f"期限: {deadline_str}\n"
                    f"\n"
                    f"====================\n"
                    f"【通知】\n"
                    f"{alert_message}\n"
                    f"===================="
                )
                
                # メール送信（アプリケーションコンテキスト内で実行）
                mail.send(msg)
                print(f"メール送信完了: {email}")
                return True
                
        except Exception as inner_e:
            print(f"メール送信内部エラー: {inner_e}")
            return False

    except Exception as e:
        print(f"メール送信エラー: {e}")
        return False