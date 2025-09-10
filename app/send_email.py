from flask_mail import Message, Mail
from flask import current_app, jsonify, request
from dotenv import load_dotenv
from flask_login import current_user
import os

load_dotenv()

def send_email():
    app = current_app
    data = request.json
    #タスク名、期限、通知メッセージの取得
    todo = data.get("todo")
    deadline = data.get("deadline")
    alert_message = data.get("alert_message")
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    mail = Mail(app)


    reception_email = current_user.email
    msg = Message(subject="通知",
                sender=app.config['MAIL_USERNAME'],
                recipients=[reception_email])
    msg.body = (
        f"タスク名: {todo}\n"
        f"期限: {deadline}\n"
        f"\n"
        f"====================\n"
        f"【通知】\n"
        f"{alert_message}です。\n"
        f"===================="
    )
    try:
        mail.send(msg)
        return jsonify({"message": "メール送信完了"}), 200
    except Exception as e:
        print(f"メール送信エラー: {e}")
        return jsonify({"error": "メール送信に失敗しました"}), 500